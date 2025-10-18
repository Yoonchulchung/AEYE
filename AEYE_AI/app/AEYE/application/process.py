import asyncio
import time
from datetime import datetime
from typing import Any, Dict

from abc import ABC, abstractmethod

import torch
from fastapi import HTTPException
from PIL import Image

from AEYE.application.AI.dataset import pil_to_tensor
from inference.domain.infer_result import Image as repoImage
from inference.domain.infer_result import InferenceResult
from inference.infra.repository.inference_repo import InferenceRepository


class IProcess(ABC):
    '''
    싱글톤으로 동작합니다. Process는 AEYE AI 서버의 요청 처리 담당입니다.
    클라이언트가 요청한 데이터를 관리하고 처리할 수 있어야 합니다. 
    
    GPU 처리 여부는 외부에서 결정합니다.
    
    Process를 통해 추론 결과를 확인할 수 없습니다. Inference DB를 통해 결과를 확인하길 바랍니다.
    '''
    
    @abstractmethod
    async def enqueue_data(self, image : Image.Image, job_id : str) -> None:
        '''
        ProcessGPU가 관리하는 큐에 데이터를 넣습니다. 
        
        큐에 넣기 전 데이터가 PIL.Image인지 확인하세요. 만약 PIL.Image 포맷이
        아니라면 에러를 발생시킵니다.
        
        큐에 넣고 요청된 정보를 Request DB에 저장합니다.
        '''
        raise NotImplementedError
    
    @abstractmethod
    async def batch_scheduler(self) -> None:
        '''
        ProcessGPU가 관리하는 큐 데이터를 이용하여 AI 추론을 진행합니다. 
        
        성능 최적화를 위해 Batch 스케줄러를 사용합니다. While 문 안에서 연속적으로 동작하는
        구조입니다. 큐에 데이터가 있으면 바로 가져오고 없으면 있을 때까지 대기합니다. 설정한
        배치 크기에 다달하면 AI 추론을 시작합니다.
        
        추론 결과는 Inference DB에 저장합니다.
        '''
        raise NotImplementedError


class ProcessGPU:
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("ProcessGPU is not initialized yet")
        return cls._instance
    
    def __init__(self, cfg_AI, cfg_HTTP, Inference, logger):
        self.cfg_AI = cfg_AI
        self.cfg_HTTP = cfg_HTTP
        
        self.logger = logger
        
        self.repo = InferenceRepository()
        
        self.inference = Inference
        
        self.BATCH_THRESHOLD = self.cfg_HTTP.BATCH_THRESHOLD
        self.BATCH_TIMEOUT = self.cfg_HTTP.BATCH_TIMEOUT
        
        self._models: Dict[str, Any] = {}
        
        self._request_lock = asyncio.Lock()
        self.request_queue = asyncio.Queue()
        
        self._model_lock = asyncio.Lock()
        self.model_queeu = asyncio.Queue()
        
        self._result_lock = asyncio.Lock()
        self.result_queue = asyncio.Queue()
        
        self._gpu_lock = asyncio.Lock()
        self.gpu_available = asyncio.Queue()
        
        if not torch.cuda.is_available():
            raise ValueError(f"ProcessGPU is only available with gpu")
        
        self.device = "cuda"
        
    
    async def add_model(self, model, gpu_id):
        async with self._model_lock:
            if model in self._models:
                self.logger(f"[ProcessGPU] {model} already loaded.")

            self._models[model] = model
            self.logger(f"")
            props = torch.cuda.get_device_properties(gpu_id)
            total_b = props.total_memory
            free_b = max(0, total_b - torch.cuda.memory_reserved(gpu_id) - torch.cuda.memory_allocated(gpu_id))
            
            self.logger(f"MEM info : Total : {float(total_b/1e9):2.2f}/{float(free_b/1e9):2.2f} GB")
            
            self.inference.set_model(model)
            
            
    async def delete_model(self, model_name):
        async with self._model_lock:
            model = self._models.pop(model_name, None)
            if model is None:
                self.logger(f"[ProcessGPU] {model_name} was not loaded.")
                return False

            try:
                # 필요한 경우 어댑터에 close/unload 훅이 있으면 호출
                if hasattr(model, "close"):
                    model.close()
                del model
            finally:
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            self.logger(f"[ProcessGPU] Unloaded {model_name}")
            return True
        
        
    async def get_result(self) -> tuple[Image.Image, str]:
        if self.result_queue.empty():
            return (None, None, None)
        else:
            img, job_id, result = await self.result_queue.get()
            #img = img[0]
            if isinstance(img, list):
                raise TypeError(f"Expected a PIL.Image.Image, but got list with length {len(img)}")
            
            return (img, job_id, result)
        
        
    async def enqueue_batch_or_tensor(self, dataset):
        
        if dataset.ndim == 4:
            async with self._request_lock:
                for img in dataset:          # shape: [N, C, H, W]
                    await self.request_queue.put(img)
        elif dataset.ndim == 3:
            async with self._request_lock:
                await self.request_queue.put(dataset)  # single image
        else:
            raise HTTPException(status_code=400, detail="Invalid tensor shape")

    async def enqueue_batch(self, dataset):
        async with self._request_lock:
            await self.request_queue.put(dataset)  # single image


    async def enque_gpu(self, id):
        await self.gpu_available.put(id)
        
    
    async def micro_batch_schdeuler(self, ):
        '''
        Make Batch until GPU is available.
        '''
        batch = []

        loop = asyncio.get_running_loop()

        while True:
            
            deadline = loop.time() + self.BATCH_TIMEOUT

            while len(batch) < self.BATCH_THRESHOLD:
                try:
                    dataset = self.request_queue.get_nowait()
                    batch.append(dataset)
                except asyncio.QueueEmpty:
                    break

            while len(batch) < self.BATCH_THRESHOLD:
                timeout = deadline - loop.time()
                if timeout <= 0:
                    break
                try:
                    dataset = await asyncio.wait_for(self.request_queue.get(), timeout=timeout)
                    batch.append(dataset)
                except asyncio.TimeoutError:
                    break
            
            if batch:
                _batch = batch.copy()
                batch = []            
                asyncio.create_task(self._run_inference(_batch, 0))

            
    async def _run_inference(self, batch, gpu_id):
        
        try:
            item = batch.pop(0)
            origin_img = item["img"]
            job_id = item["job_id"]
        except IndexError:
            print("No items in batch.")
            return
        
        start_time = time.time()
        loop = asyncio.get_event_loop()
        img = pil_to_tensor(origin_img).to('cuda')
        async with self._model_lock:
            result = await loop.run_in_executor(None, self.inference, img)
        async with self._result_lock:
            await self.result_queue.put((origin_img, job_id, result))
            
            now = datetime.now()
            result = InferenceResult(
                job_id=job_id,
                result=result["llm_result"],
                classification=result["pred"],
                created_at=now,
                updated_at=now,
            )
            
            # image = repoImage(
                
            # )
            self.repo.save(result)