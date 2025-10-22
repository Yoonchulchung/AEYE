import os

from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import serializers

from ai.models import AIVersion
from ai.serializers import AIVersionSerializer

from patient.models import Patient

from ..models import Checkup, Diagnosis, OCTImage


class OCTImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OCTImage
        fields = ['image']

# class DiagnosisInfoSerializer(serializers.ModelSerializer):
#     ai_version = AIVersionSerializer(required=False)

#     class Meta: 
#         model=DiagnosisInfo
#         fields = '__all__'

#     @transaction.atomic
#     def create(self, validated_data):
#         ai_data = validated_data.pop("ai_version", None)
#         diagnosis = super().create(validated_data)

#         if ai_data:
#             if diagnosis.kind != DiagnosisInfo.Kind.AI:
#                 raise serializers.ValidationError({"ai_version": "AI 진단일 때만 ai_version을 저장할 수 있습니다."})
#             AIVersion.objects.create(diagnosis=diagnosis, **ai_data)
#         return diagnosis

#     def update(self, instance, validated_data):
#         ai_data = validated_data.pop("ai_version", None)
#         diagnosis = super().update(instance, validated_data)

#         if ai_data is not None:
#             if diagnosis.kind != DiagnosisInfo.Kind.AI:
#                 raise serializers.ValidationError({"ai_version": "AI 진단일 때만 ai_version을 수정할 수 있습니다."})

#             if hasattr(diagnosis, "ai_version"):
#                 for k, v in ai_data.items():
#                     setattr(diagnosis.ai_version, k, v)
#                 diagnosis.ai_version.full_clean()
#                 diagnosis.ai_version.save()
#             else:
#                 AIVersion.objects.create(diagnosis=diagnosis, **ai_data)
#         return diagnosis
    

        
class CheckupNewWriteSerializer(serializers.ModelSerializer):
    '''
    새로운 환자 정보를 추가합니다.
    
    Request Body:
    {
        "patient_id": "환자 ID",
        "user_id": "사용자 ID",
        "meta": {
            "eye_side": "R",
        }
        "image": "이미지 데이터",
    } 
    
    '''
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model=Checkup
        fields = ["patient", "id", "image"]
    
    def validate_image(self, files):
        if not files:
            raise serializers.ValidationError("최소 1개의 이미지는 필요합니다.")
        return files
    
    @transaction.atomic
    def create(self, validated_data):
        img = validated_data.pop("image", [])
        checkup = super().create(validated_data)
        
        if img is not None:
            
            if not img.name.lower().endswith(('.jpg', '.jpeg', '.png', '.dcm')):
                raise ValueError("Wrong image format is inserted to Checkup Serializere")
            
            patient = checkup.patient
            ts = timezone.localtime().strftime("%Y%m%d_%H%M%S")
            base = f"{ts}_{patient.id}"
            ext = os.path.splitext(img.name)[1].lower() or ".jpg"
            img.name = f"{base}{ext}"

            OCTImage.objects.create(image=img)
        
        return checkup

    