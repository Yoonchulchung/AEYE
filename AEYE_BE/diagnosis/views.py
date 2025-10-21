import time

import httpx
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from asgiref.sync import async_to_sync

from .models import Checkup
from .serializers import CheckupSerializer, DiagnosisInfoSerializer

import io


class DiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = CheckupSerializer
     
    def get_queryset(self):
        return (
            Checkup.objects
            .order_by("-created_at")
        )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        client_serializer = CheckupSerializer(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        checkup = client_serializer.save()

        # infer_result = async_to_sync(self._test_inference_image)(
        #     client_serializer.validated_data.get('image'))
        
        infer_result = async_to_sync(self._inference_image)(
            client_serializer.validated_data.get('image')
        )
        
        payload = {
            "checkup" : checkup.id,
            "kind" : "AI",
            "status" : "LR",
            "result" : infer_result.get("result"),
            "classification" : infer_result.get("classification")   
        }
        
        # infer_serializer = DiagnosisInfoSerializer(data=payload)
        # infer_serializer.is_valid(raise_exception=True)
        # infer = infer_serializer.save()
            
        return Response(
            {'message' : infer_result.get("result")},
            status=status.HTTP_200_OK,
        )
    
    async def _test_inference_image(self, image):
        payload = {
            "result" : "GOOD",
            "classification" : "GOOD"
        }
        return payload
    
    async def _inference_image(self, image):
        ai_diagnose_url = "http://0.0.0.0:2000/api/v1/inference"

        start = time.monotonic()
        timeout_s = 10
        job_id = await self._request_infernce(image, ai_diagnose_url)

        print(job_id)
        ai_result_url = f"http://0.0.0.0:2000/api/v1/inference/result/{job_id}"
        while True:
            infer_result = await self._get_inference_result(url=ai_result_url)
            
            status = infer_result.get("status")
            if status == "SUCCESS":
                return infer_result
            if time.monotonic() - start > timeout_s:
                raise TimeoutError(f"Timed out waiting for job {job_id}")
            
    # async def _request_infernce(self, image, url):
        
    #     image = convert_django_image_to_pil(image)
    #     async with httpx.AsyncClient() as client:
    #         resp = await client.post(url, data={'image' : image})
        
    #         if resp.status_code not in (200, 202):
    #             resp.raise_for_status()
    #         data = resp.json()
    #         job_id = data.get("job_id")
            
    #     return job_id
    async def _request_infernce(self, image, url):
        
        pil_image = convert_django_image_to_pil(image)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG") 
        image_bytes = buffer.getvalue() 

        headers = {
            'Content-Type': 'application/octet-stream'
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, content=image_bytes, headers=headers, timeout=30.0)
        
            if resp.status_code not in (200, 202):
                resp.raise_for_status()
            data = resp.json()
            job_id = data.get("job_id")
            
            return job_id
    
    async def _get_inference_result(self, url):
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            
            if resp.status_code not in (200, 202):
                resp.raise_for_status()
            data = resp.json()
            return data
        

from PIL import Image
def convert_django_image_to_pil(django_image_file):
    
    if not django_image_file:
        return None

    try:    
        pil_image = Image.open(django_image_file.file)
        return pil_image
    except Exception as e:
        print(f"Error converting image to PIL: {e}")
        return None