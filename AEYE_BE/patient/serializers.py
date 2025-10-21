from rest_framework import serializers

from .models import Patient
from diagnosis.serializers import CheckupSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__" 
        
class PatientSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields=['name', 'DOB']
        
class PatientDiagnoseSerializer(serializers.ModelSerializer):
    checkups = CheckupSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "name", "DOB", "checkups"]