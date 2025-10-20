import asyncio
import time
from datetime import datetime
from typing import Any, Dict

from abc import ABC, abstractmethod

import torch
from fastapi import HTTPException

from AEYE.application.AI.dataset import pil_to_tensor
from inference.domain.result import Result
from inference.infra.repository.result_repo import ResultRepository
from inference.domain.request import Request
from inference.infra.repository.request_repo import RequestRepository


class IProcess(ABC):
    '''
    싱글톤으로 동작합니다. Process는 AEYE AI 서버의 요청 처리 담당입니다.
    클라이언트가 요청한 데이터를 관리하고 처리할 수 있어야 합니다. 
    
    GPU 처리 여부는 외부에서 결정합니다.
    
    Process를 통해 추론 결과를 확인할 수 없습니다. Inference DB를 통해 결과를 확인하길 바랍니다.
    '''
    
    @abstractmethod
    async def enqueue_request(self, dataset : dict) -> None:
        '''
        ProcessGPU가 관리하는 큐에 데이터를 넣습니다. 
        
        dataset의 형태는 {"img" : Image, "job_id" : "Job ID"} 입니다.
        
        큐에 넣기 전 데이터가 torch.Tensor인지 확인하세요. 만약 torch.Tensor 포맷이
        아니라면 에러를 발생시킵니다. 큐에는 이미지 한 장씩 넣습니다.
        
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


class Process:
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Process is not initialized yet")
        return cls._instance
    
    def __init__(self, cfg, Inference, logger):
        
        self.cfg_HTTP = cfg.HTTP
        
        self.logger = logger
        
        self.request_repo = RequestRepository()
        self.result_repo = ResultRepository()

        
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
        
        if not torch.cuda.is_available():
            raise ValueError(f"ProcessGPU is only available with gpu")
        
        self.device = "cuda"


    async def enqueue_request(self, dataset : dict) -> None:
        
        if not isinstance(dataset["img"], torch.Tensor):
            raise ValueError(f"Please enqueue torch.Tensor format.")
        
        async with self._request_lock:
            await self.request_queue.put(dataset)
            
        self._save_request(dataset)
        
    def _save_request(self, dataset):
        self.request_repo.save(dataset["img"], dataset["job_id"])
    
    async def batch_scheduler(self) -> None:
        
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
                asyncio.create_task(self._run_inference(_batch))

            
    async def _run_inference(self, batch):
        
        try:
            item = batch.pop(0)
            job_id = item["job_id"]
        except IndexError:
            print("No items in batch.")
            return
        
        img : torch.Tensor = item["img"].unsqueeze(0).to(self.device)
        
        loop = asyncio.get_event_loop()
        async with self._model_lock:
            result = await loop.run_in_executor(None, self.inference, img)
        
        self._save_result(result, job_id)
            
    def _save_result(self, result, job_id):
        result = Result(
            job_id=job_id,
            result=result["llm_output"],
            classification=result["cls_output"],
            result_summary=result["diagnosis_summary"],
        )
        
        self.result_repo.save(result)