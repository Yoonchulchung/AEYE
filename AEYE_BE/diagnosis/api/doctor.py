from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from ..models import Checkup
from ..serializer.request import DiagnosisDoctorRequestSerializer
from ..serializer.write import (CheckupNewWriteSerializer,
                                DiagnosisDoctorNewWriteSerializer,
                                OCTImageWriteSerializer)


class DoctorDiagnosis(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    '''
    의사 추론 요청 API 입니다. 
    
    DiagnosisDoctorViewSet DiagnosisDoctorAddViewSet 사용할 수 있습니다.
    
    - DiagnosisDoctorViewSet : 처음 환자 진료를 추가하는 경우입니다.
    - DiagnosisDoctorAddViewSet : 이전 진료기록이 있는 경우에 진료를 추가하는 경우입니다.
    
    '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.ai_diagnosis_url = "http://0.0.0.0:2000/api/v1/inference"
        self.headers = {
            'Content-Type': 'application/octet-stream'
        }
        self.timeout_s = 5
    
    
class DiagnosisDoctorViewSet(DoctorDiagnosis):

    serializer_class = DiagnosisDoctorRequestSerializer
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
        oct_img_serializer.save()
                
        try:
            payload = _save_diagnosis_result(client_data)
                        
        except Exception as e:
            payload = {
                        "error": {
                            "code": "INFERENCE_FAILED",
                            "message": "AI model inference failed or an unexpected error occurred.",
                            "details": str(e),
                        },
                    }
            
        return Response(data=payload, status=status.HTTP_200_OK)
        
            
def _save_diagnosis_result(client_data):
        payload = {
            "checkup_id": client_data.get("checkup_id"),
            "kind": "DR",
            "status": "MR",
            "classification": client_data.get("classification"),
            "result": client_data.get("result"),
        }
        
        diagnosis_serializer = DiagnosisDoctorNewWriteSerializer(data=payload)
        diagnosis_serializer.is_valid(raise_exception=True)
        diagnosis_serializer.save()
        
        return diagnosis_serializer.data