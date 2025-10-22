from rest_framework import serializers

from diagnosis.models import Checkup
from patient.models import Patient


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    eye_side = serializers.CharField(write_only=True)
    oct_img = serializers.ImageField(write_only=True)
    
    class Meta:
        model = Checkup
        fields = ["patient_id", "eye_side", "oct_img"]