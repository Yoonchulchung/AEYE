import time

import httpx
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from asgiref.sync import async_to_sync
from PIL import Image

from ..models import Checkup
from ..serializer.write import OCTImageWriteSerializer, CheckupNewWriteSerializer, \
                               DianosisAIWriteSerializer

import io


class AIDiagnosis(APIView):
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

        ai_result_url = f"{self.ai_diagnosis_url}/{job_id}"
        while True:
            infer_result = await self._get_infer_result(url=ai_result_url)
            
            status = infer_result.get("status")
            if status == "SUCCESS":
                return infer_result
            elif status == "WAITING":
                ...
            else:
                raise ValueError(infer_result)
            
            if time.monotonic() - start > self.timeout_s:
                raise TimeoutError(f"Timed out waiting for job {job_id}")
            
    async def _req_infer(self, img, url):
        
        img_bytes = _img_to_bytes(img)
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, content=img_bytes, headers=self.headers, timeout=30.0)
        
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

    def get_queryset(self):
        return (
            Checkup.objects
            .order_by("-created_at")
        )
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client_data = request.data.copy()

        checkup_serializer = CheckupNewWriteSerializer(data=client_data)
        checkup_serializer.is_valid(raise_exception=True)
        checkup = checkup_serializer.save()
        
        client_data["checkup_id"] = checkup.id
        
        oct_img_serializer = OCTImageWriteSerializer(data=client_data)
        oct_img_serializer.is_valid(raise_exception=True)
        oct_img = oct_img_serializer.save()
        
        img = oct_img.validated_data.get('oct_img')
        
        infer_result = async_to_sync(self._infer_img)(img)
        
        try:
            diagnosis = _save_diagnosis_result(checkup, infer_result)
            payload = {
                
            }
        except Exception:
            payload = {
                    "error": {
                        "code": "INVALID_IMAGE",
                        "message": "Image is corrupted or not supported.",
                        "patient_id": "환자 ID",
                        "details": {
                            "allowed_extensions" : ["jpg","png","dcm"] 
                        },
                    },
                    }
        
        return Response(data=payload, status=status.HTTP_200_OK)
        

def _img_to_bytes(img_file) -> io.BytesIO:

    buffer = io.BytesIO()

    try:    
        pil_image = Image.open(img_file.file)
        pil_image.save(buffer, format="JPEG") 
        return buffer.getvalue() 
        
    except Exception as e:
        print(f"Error converting image to PIL: {e}")
        return None
    
    
def _save_diagnosis_result(self, checkup, infer_result):
        payload = {
            "checkup_id": checkup.id,
            "kind": "AI",
            "status": infer_result.get("status"),
            "classification": infer_result.get("classification"),
            "result": infer_result.get("result"),
            "result_summary": infer_result.get("result_summary")   
        }
        
        infer_serializer = DianosisAIWriteSerializer(data=payload)
        infer_serializer.is_valid(raise_exception=True)
        return infer_serializer.save()