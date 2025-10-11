from rest_framework import serializers

from ai.models import AIVersion
from ai.serializers import AIVersionSerializer

from .models import Checkup, DiagnosisInfo, OCTImage


class OCTImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OCTImage
        field = ['image']

class DiagnosisInfoSerializer(serializers.ModelSerializer):
    ai_version = AIVersionSerializer(required=False)

    class Meta: 
        model=DiagnosisInfo
        field = '__all__'


    def create(self, validated_data):
        ai_data = validated_data.pop("ai_version", None)
        diagnosis = super().create(validated_data)

        if ai_data:
            if diagnosis.kind != DiagnosisInfo.Kind.AI:
                raise serializers.ValidationError({"ai_version": "AI 진단일 때만 ai_version을 저장할 수 있습니다."})
            AIVersion.objects.create(diagnosis=diagnosis, **ai_data)
        return diagnosis

    def update(self, instance, validated_data):
        ai_data = validated_data.pop("ai_version", None)
        diagnosis = super().update(instance, validated_data)

        if ai_data is not None:
            if diagnosis.kind != DiagnosisInfo.Kind.AI:
                raise serializers.ValidationError({"ai_version": "AI 진단일 때만 ai_version을 수정할 수 있습니다."})

            if hasattr(diagnosis, "ai_version"):
                for k, v in ai_data.items():
                    setattr(diagnosis.ai_version, k, v)
                diagnosis.ai_version.full_clean()
                diagnosis.ai_version.save()
            else:
                AIVersion.objects.create(diagnosis=diagnosis, **ai_data)
        return diagnosis
    
class CheckupSerializer(serializers.ModelSerializer):
    diagnoses = DiagnosisInfoSerializer(many=True, read_only=True)

    class Meta:
        model=Checkup
        fields = ["id", "date", "patient"]
        
class DiagnosisFlatSerializer(serializers.ModelSerializer):
    checkup_id  = serializers.IntegerField(source="checkup.id", read_only=True)
    patient_id  = serializers.IntegerField(source="checkup.patient.id", read_only=True)
    patient_name = serializers.CharField(source="checkup.patient.name", read_only=True)

    class Meta:
        model = DiagnosisInfo
        fields = ["id", "kind", "status", "result", "classification",
                  "checkup_id", "patient_id", "patient_name", "created_at"]