import time

import httpx
from asgiref.sync import async_to_sync
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from utils.dataset import img_to_bytes

from ..models import Checkup
from ..serializer.request import DiagnosisAIRequestSerializer
from ..serializer.write import (CheckupNewWriteSerializer,
                                DiagnosisAIWriteSerializer,
                                OCTImageWriteSerializer)


class AIDiagnosis(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    '''
    AI 추론 요청 API 입니다. 
    
    DiagnosisAIViewSet과 DiagnosisAIAddViewSet을 사용할 수 있습니다.
    
    - DiagnosisAIViewSet : 처음 환자 진료를 추가하는 경우입니다.
    - DiagnosisAIAddViewSet : 이전 진료기록이 있는 경우에 진료를 추가하는 경우입니다.
    
    '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.ai_diagnosis_url = "http://0.0.0.0:2000/api/v1/inference"
        self.headers = {
            'Content-Type': 'application/octet-stream'
        }
        self.timeout_s = 5
        
        
    async def _infer_img(self, img):

        start  = time.monotonic()
        job_id = await self._req_infer(img, self.ai_diagnosis_url)

        ai_result_url = f"{self.ai_diagnosis_url}/result/{job_id}"
        while True:
            infer_result = await self._get_infer_result(url=ai_result_url)
            
            status = infer_result.get("status")
            if status == "SUCCESS":
                return infer_result
            elif status == "WAIT":
                ...
            else:
                raise ValueError(infer_result)
            
            if time.monotonic() - start > self.timeout_s:
                raise TimeoutError(f"Timed out waiting for job {job_id}")
            
    async def _req_infer(self, img, url):
        
        img_bytes = img_to_bytes(img)
        headers = {
            'Content-Type': 'application/octet-stream'
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, content=img_bytes, headers=headers, timeout=30.0)
        
        if resp.status_code not in (200, 202):
            resp.raise_for_status()
        return resp.json().get("job_id")
        
    async def _get_infer_result(self, url : str):
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            
        if resp.status_code not in (200, 202):
            resp.raise_for_status()
        return resp.json()
    
    
class DiagnosisAIViewSet(AIDiagnosis):

    serializer_class = DiagnosisAIRequestSerializer
    queryset = Checkup.objects.order_by("-created_at")
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        client_data = request.data.copy()

        checkup_serializer = CheckupNewWriteSerializer(data=client_data)
        checkup_serializer.is_valid(raise_exception=True)
        checkup = checkup_serializer.save()
        
        client_data["checkup_id"] = checkup.id
        
        oct_img_serializer = OCTImageWriteSerializer(data=client_data)
        oct_img_serializer.is_valid(raise_exception=True)
        oct_img = oct_img_serializer.save()
        
        img = oct_img.oct_img
        
        infer_result = async_to_sync(self._infer_img)(img)
        
        try:
            payload = _save_diagnosis_result(checkup, infer_result)
                        
        except Exception as e:
            payload = {
                        "error": {
                            "code": "INFERENCE_FAILED",
                            "message": "AI model inference failed or an unexpected error occurred.",
                            "details": str(e),
                        },
                    }
            
        return Response(data=payload, status=status.HTTP_200_OK)
    
    
def _save_diagnosis_result(checkup, infer_result):
        payload = {
            "checkup_id": checkup.id,
            "kind": "AI",
            "status": "MR",
            "classification": infer_result.get("classification"),
            "result": infer_result.get("result"),
            "result_summary": infer_result.get("summary")   
        }
        
        diagnosis_serializer = DiagnosisAIWriteSerializer(data=payload)
        diagnosis_serializer.is_valid(raise_exception=True)
        diagnosis_serializer.save()
        
        return diagnosis_serializer.data