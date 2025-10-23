from rest_framework import serializers

from ai.models import AIVersion
from ai.serializers import AIVersionSerializer

from ..models import Checkup, Diagnosis
from .serializer import (CheckupMetaSerializer, DiagnosisSerializer,
                         OCTImageSerializer)


class DiagnosisReadSerializer(serializers.ModelSerializer):
    '''
    Response Body:
    {
        "date": "진료 일자", 
        "kind": "AI",
        "status": "환자 상태",
        "classification": "병 이름",
        "result": "진단 결과",
        "result_summary": "진단 결과 요약",   
        "ai_version": {
		    "model_name": "AI 모델 이름",
		    "model_weight": "AI에 사용된 가중치 이름",
		    "probability": "AI 모델 정확도",
		    "version": "AI 모델 버젼",
		}
    }
    
    위 결과에서 ai_version은 존재하지 않을 수 있습니다.
    '''
    
    ai_version = serializers.SerializerMethodField()
    
    class Meta:
        model=Diagnosis
        fields = ["date", "kind", "status", "classification", 
                  "result", "result_summary", "ai_version"]

    def get_ai_version(self, obj):
        
        try:
            ai_version_instance = obj.ai_version            
            return AIVersionSerializer(ai_version_instance).data
        except AIVersion.DoesNotExist:
            return None


class CheckupReadSerializer(serializers.ModelSerializer):
    '''
    
    Response Body:
    {
        "checkup_id": "진료 ID",
        "patient_name": "환자 이름",
        "oct_image": {
            "oct_img": ""
        },
        "meta": {
            "eye_side": "RIGHT"
        },
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
    }

    위 결과에서 ai_version은 존재하지 않을 수 있습니다.
    '''
    patient_name = serializers.CharField()
    diagnosis = DiagnosisSerializer(many=True, read_only=True)
    oct_image = OCTImageSerializer(many=True, read_only=True)
    meta = CheckupMetaSerializer(many=True, read_only=True)
    
    class Meta:
        model=Checkup
        fields = ["checkup_id", "patient_name", "oct_image", "meta", "diagnosis" ] 
    