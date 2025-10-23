from rest_framework import serializers

from diagnosis.models import Checkup
from patient.models import Patient


class DiagnosisAIRequestSerializer(serializers.ModelSerializer):
    '''
    클라이언트가 POST /diagnosis/ai 로 데이터를 업로드하면
    DiagnosisAIRequestSerializer 로 요청을 검사합니다.
    
    Request Body:
    {
        "patient_id" : "환자 ID",
        "eye_side": "right", 
        "data": {
            "image" : "<base64_encoded_OCT_image>"
        },
    }
    '''
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    eye_side = serializers.CharField(write_only=True)
    oct_img = serializers.ImageField(write_only=True)
    
    class Meta:
        model = Checkup
        fields = ["patient_id", "eye_side", "oct_img"]
        

class DiagnosisDoctorRequestSerializer(serializers.ModelSerializer):
    '''
    클라이언트가 POST /diagnosis/doctor 로 데이터를 업로드하면
    DiagnosisDoctorRequestSerializer 로 요청을 검사합니다.
    
    Request Body:
    {
        "patient_id" : "환자 ID",
        "eye_side": "right", 
        "data": {
            "image" : "<base64_encoded_OCT_image>"
        },
        "status" : "환자 상태",
        "result" : "진료 결과",
        "classification" : "병 이름",
    }
    '''
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    eye_side = serializers.CharField(write_only=True)
    oct_img = serializers.ImageField(write_only=True)
    status = serializers.CharField(write_only=True)
    result = serializers.CharField(write_only=True)
    classification = serializers.CharField(write_only=True)
    
    class Meta:
        model = Checkup
        fields = ["patient_id", "eye_side", "oct_img", "status",
                  "result", "classification"]