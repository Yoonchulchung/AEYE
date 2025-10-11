from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Patient
from .serializers import PatientSaveSerializer, PatientSerializer, \
                         PatientDiagnoseSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PatientSaveSerializer
        return PatientSerializer
    
    def get_queryset(self):
        return (Patient.objects
                .filter(db_status=True)                
                .order_by('-recent_visit_date', '-id'))
        
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        serializer = PatientSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get("name")
        dob = serializer.validated_data.get("DOB")

        patient, created = Patient.objects.get_or_create(
            name=name,
            DOB=dob,
        )

        if created:
            message = "Succeeded to save patient."
        else:
            message = "Patient is already registered."
            
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message' : message},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            headers=headers
        )

    @action(detail=True, methods=['get'], url_path='diagnoses')
    def diagnoses(self, request, pk=None):
        from diagnose.models import DiagnosisInfo
        qs = (DiagnosisInfo.objects
              .filter(checkup__patient_id=pk)
              .select_related("checkup", "checkup__patient")
              .order_by("-created_at"))
        page = self.paginate_queryset(qs)
        from diagnose.serializers import DiagnosisFlatSerializer
        if page is not None:
            return self.get_paginated_response(DiagnosisFlatSerializer(page, many=True).data)
        return Response(DiagnosisFlatSerializer(qs, many=True).data)