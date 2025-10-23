import os

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from diagnosis.serializer.read import CheckupReadSerializer

from .models import Patient


class PatientWriteSerializer(serializers.ModelSerializer):
    '''
    신규 환자를 추가합니다.
    Request Body:
    {
        "name" : "환자 이름",
        "DOB" : "환자 생일 (YY-MM-DD)",
        "profile_image" : "환자 이미지",
    }
    '''
    
    class Meta:
        model=Patient
        fields=["name", "DOB", "profile_image"]

    def validate_profile_image(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.jpeg', '.png', '.dcm']
        
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError("지원하지 않는 이미지 형식입니다. jpg, jpeg, png, dcm 파일만 업로드할 수 있습니다.")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        name = validated_data.pop("name")
        DOB = validated_data.pop("DOB")
        profile_image = validated_data.pop("profile_image")
        
        ts = timezone.localtime().strftime("%Y%m%_d_%H%M%S")
        base = f"{ts}_{name}"
        ext = os.path.splitext(profile_image.name)[1].lower() or ".jpg"
        profile_image.name = f"{base}{ext}"
        
        return Patient.objects.create(name=name,
                                      DOB=DOB,
                                      profile_image=profile_image)
    
    
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
    
    patient_id = serializers.IntegerField(source='id')
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
    
    patient_id = serializers.CharField(source='id')
    patient_name = serializers.CharField(source='name')
    checkup = CheckupReadSerializer(read_only=True, many=True)
    
    class Meta:
        model=Patient
        fields=["patient_id", "patient_name", "DOB", "profile_image",
                "visit_nums", "recent_visit", "severity_percentage", 
                "status", "checkup"]