from rest_framework import serializers

from .models import Patient
from diagnosis.serializer.read import CheckupReadSerializer


class PatientReadSerializer(serializers.ModelSerializer):
    '''
    환자의 정보만 조회할 수 있습니다.
    
    Response Body:
    {
        "patient_id": "환자 ID",
        "patient_name": "환자 이름",
        "DOB" : "2000.03.18",
        "profile_image" : "https://i.pravatar.cc/307",
        "visit_nums": 3,
        "recent_visit": "2024.07.10",
        "severity_percentage": "60%",
        "status": "MODERATE_RISK",
    }
    '''
    
    Patient_id = serializers.CharField(source='id')
    patient_name = serializers.CharField(source='name')
    
    class Meta:
        model=Patient
        fields=["patient_id", "patient_name", "DOB", "profile_image",
                "visit_nums", "recent_visit", "severity_percentage", 
                "status"]
        
    
class PatientReadAllSerializer(serializers.ModelSerializer):
    '''
    환자의 모든 정보를 조회할 수 있습니다.
    
    Response Body:
    {  
        "patient_id": "환자 ID",
        "patient_name": "환자 이름",
        "DOB" : "2000.03.18",
        "profile_image" : "https://i.pravatar.cc/307",
        "visit_nums": 3,
        "recent_visit": "2024.07.10",
        "severity_percentage": "60%",
        "status": "MODERATE_RISK",
        "checkup":{
            {
                "checkup_id": "진료 ID",
                "patient_name": "환자 이름",
                "meta" : {
                    "eye_side": "RIGHT"
                }
                "OCT_images" : {
                    "oct_img" : ""
                }
                "diagnosis": {
                    "date": "진료 일자", 
                    "kind": "AI",
                    "status": "환자 상태",
                    "classification": "병 이름",
                    "result": "진단 결과",
                    "result_summary": "진단 결과 요약",
                    "ai_version": {
                        "model_name": "AI 모델 이름",
                        "model_weight": "AI에 사용된 가중치 이름",
                        "probability": 
                        "AI 모델 정확도",
                        "version": "AI 모델 버젼",
                    }
                }
            }, {...}
        },
    }
    
    ai_version은 없을 수 있습니다.
    '''
    
    Patient_id = serializers.CharField(source='id')
    patient_name = serializers.CharField(source='name')
    checkup = CheckupReadSerializer(read_only=True, many=True)
    
    class Meta:
        model=Patient
        fields=["patient_id", "patient_name", "DOB", "profile_image",
                "visit_nums", "recent_visit", "severity_percentage", 
                "status", "checkup"]