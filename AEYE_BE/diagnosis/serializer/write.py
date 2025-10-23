import os
from datetime import datetime

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from ai.models import AIVersion
from patient.models import Patient

from ..models import Checkup, CheckupMeta, Diagnosis, OCTImage


class CheckupNewWriteSerializer(serializers.ModelSerializer):
    '''
    새로운 환자 진료 기록을 추가합니다.
    
    Request Body:
    {
        "patient_id" : "환자 ID"
    }
    '''
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model=Checkup
        fields = ["patient_id"]
    
    @transaction.atomic
    def create(self, validated_data):
        patient_instance = validated_data.pop('patient_id')
        
        now = datetime.now()
        
        return Checkup.objects.create(patient=patient_instance,
                              date=now)
    
    
class OCTImageWriteSerializer(serializers.ModelSerializer):
    '''
    진료 기록의 OCT 이미지를 기록합니다. 환자가 중복되어서 데이터가 저장될 수 있기 떄문에
    환자 ID를 입력받아 image path에 함께 저장합니다. 
    
    Checkup DB -> OCTImage DB
    
    Checkup DB를 먼저 저장하고, OCTImage DB에 저장해야 합니다.
    
    Request Body:
    {
        "oct_img" : "[jpg, jpeg, png, dcm] 포맷만 허용됩니다."
        "checkup_id" : "Checkup DB에서 할당 받은 진료 ID"
        "patient_id" : "클라이언트가 입력한 환자 ID"
    }
    '''
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    checkup_id = serializers.PrimaryKeyRelatedField(queryset=Checkup.objects.all())
    
    class Meta:
        model = OCTImage
        fields = ['oct_img', 'checkup_id', 'patient_id']
        
    def validate_oct_img(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.jpeg', '.png', '.dcm']
        
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError("지원하지 않는 이미지 형식입니다. jpg, jpeg, png, dcm 파일만 업로드할 수 있습니다.")
        return value
        
    @transaction.atomic
    def create(self, validated_data):
        oct_img = validated_data.pop('oct_img')
        
        checkup_instance = validated_data.pop('checkup_id')        
        patient_instance = validated_data.pop('patient_id')
        
        ts = timezone.localtime().strftime("%Y%m%   d_%H%M%S")
        base = f"{ts}_{patient_instance.id}_{checkup_instance.id}"
        ext = os.path.splitext(oct_img.name)[1].lower() or ".jpg"
        oct_img.name = f"{base}{ext}"

        return OCTImage.objects.create(checkup=checkup_instance,
                                       oct_img=oct_img,
                                        **validated_data)
    

class CheckupMetaWriteSerializer(serializers.ModelSerializer):
    '''
    환자의 진료 meta 정보를 기입합니다.
    
    '''
    checkup_id = serializers.PrimaryKeyRelatedField(queryset=Checkup.objects.all()) 

    class Meta:
        model = CheckupMeta
        fields = ["checkup_id", "eye_side"]

class DiagnosisAIWriteSerializer(serializers.ModelSerializer):
    '''
    AI 진단 이후 진단 정보를 기록합니다.
    
    Checkup DB -> Diagnosis DB
    
    Checkup DB를 먼저 저장하고, Diagnosis DB를 저장합니다.
    
    Request Body:
    {
        "checkup_id" : "진료 ID",
        "kind" : "['AI', 'DR', 'RE'] 중 하나만 선택",
        "status" : "['MR', 'LR', 'HR'] 중 하나만 선택",
        "classification" : "병 이름",
        "result" : "진단 결과",
        "reuslt_summary" : "진단 결과 요약"
    }
    '''
    checkup_id = serializers.PrimaryKeyRelatedField(queryset=Checkup.objects.all()) 
       
    class Meta:
        model  = Diagnosis
        fields = ["checkup_id", "kind", "status", "classification",
                  "result", "result_summary"]
    
    def validate_kind(self, value):
        if value != "AI":
            raise serializers.ValidationError("AI 진단만 기록이 가능합니다.")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        
        checkup_instance = validated_data.pop("checkup_id")
        diagnosis_instance = Diagnosis.objects.create(
            checkup=checkup_instance,
            **validated_data)
        
        AIVersion.objects.create(
            diagnosis=diagnosis_instance,
            oct_model_name="OCTD",
            oct_model_weight="best_validated_model",
            oct_probability=98,
            oct_version="0.1",
            llm_model_name="OpenAI",
            llm_model_weight="GPT-4o",
        )
        
        return diagnosis_instance
    
    
class DiagnosisDoctorNewWriteSerializer(serializers.ModelSerializer):
    '''
    신규 환자의 의사 진단을 기록합니다.
    
    Checkup DB -> Diagnosis DB
    
    Checkup DB를 먼저 저장하고, Diagnosis DB를 저장합니다.
    
    Request Body:
    {
        "checkup_id" : "진료 ID",
        "kind" : "['AI', 'DR', 'RE'] 중 하나만 선택",
        "status" : "['MR', 'LR', 'HR'] 중 하나만 선택",
        "classification" : "병 이름",
        "result" : "진단 결과",
    }
    '''
    checkup_id = serializers.PrimaryKeyRelatedField(queryset=Checkup.objects.all()) 
       
    class Meta:
        model  = Diagnosis
        fields = ["checkup_id", "kind", "status", "classification",
                  "result"]
    
    @transaction.atomic
    def create(self, validated_data):
        
        checkup_instance = validated_data.pop("checkup_id")
        diagnosis_instance = Diagnosis.objects.create(
            checkup=checkup_instance,
            **validated_data)
        
        return diagnosis_instance