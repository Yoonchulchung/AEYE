from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient
from diagnosis.models import Checkup
from .serializers import PatientReadSerializer, PatientWriteSerializer, PatientReadAllSerializer

class PatientViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    
    queryset = Patient.objects.all()
    serializer_class = PatientWriteSerializer
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PatientReadSerializer
        return PatientWriteSerializer
    
    def retrieve(self, request, *args, **kwargs):
        '''
        특정 환자를 조회합니다.
        '''
        
        patient = self.get_object()
        serializer = self.get_serializer(patient)
        return Response(serializer.data)
        
    def list(self, request, *args, **kwargs):
        '''
        모든 환자를 조회합니다.
        '''
        
        qs = self.get_queryset()
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)
        
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        '''
        신규 환자를 추가합니다.
        
        Request Body :
        {
            "name" : "환자 이름",
            "DOB" : "환자 생일 (YY-MM-DD)",
            "profile_image" : "환자 이미지 URL",
        }
        '''
        
        try:
            patient_serializer = PatientWriteSerializer(data=request.data)
            patient_serializer.is_valid(raise_exception=True)
            patient_serializer.save()
            
            payload = {
                "status" : "SUCCESS"
            }
        except Exception as e:
            payload = {
                "status" : "ERROR",
                "message" : str(e),
            }

        return Response(data=payload, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'], url_path='checkup')
    def checkups(self, request, pk=None):
        '''
        특정 환자 진단 결과 조회
        '''
            
        queryset = Patient.objects.filter(pk=pk).prefetch_related(
            'checkup',
            'checkup__oct_image',
            'checkup__meta',
            'checkup__diagnosis'
        ).order_by('-created_at')
        
        serializer = PatientReadAllSerializer(queryset, many=True)
        
        return Response(serializer.data)