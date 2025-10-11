from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import Patient
from .serializers import PatientSerializer, PatientSaveSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSaveSerializer

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
