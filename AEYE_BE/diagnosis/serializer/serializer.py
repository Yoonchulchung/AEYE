from rest_framework import serializers
from ..models import Diagnosis, OCTImage, CheckupMeta

class DiagnosisSerializer(serializers.ModelSerializer):
    '''
    Response Body:
    {
        "date" : "진료 일자", 
        "kind": "AI",
        "status": "환자 상태",
        "classification": "병 이름",
        "result": "진단 결과",
        "result_summary": "진단 결과 요약",   
    }
    '''
    class Meta:
        model=Diagnosis
        fields = ["date", "kind", "status", "classification", "result", "result_summary"]
        
class OCTImageSerializer(serializers.ModelSerializer):
    '''
    Response Body:
    {
        "oct_img" : ""
    }
    '''
    
    class Meta:
        model=OCTImage
        fields=["oct_img"]
        
class CheckupMetaSerializer(serializers.ModelSerializer):
    '''
    Response Body:
    {
        "eye_side" : "RIGHT"
    }
    '''
    
    class Meta:
        model=CheckupMeta
        fields=["eye_side"]