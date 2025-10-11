from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import OCTImageSerializer
from .models import DiagnosisInfo


class DiagnoseViewSet(viewsets.ModelViewSet):
    
    
    def get_queryset(self):
        return (
            DiagnosisInfo.objects
            .select_related("checkup", "checkup__patient")
            .order_by("-created_at")
        )
        
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = OCTImageSerializer(data=request.data)
        
        ai_diagnose_url = "http://localhost:3000/v1/api/upload/pil"

        headers = self.get_success_headers(serializer.data)

        return Response(
            {'message' : "GOOD"},
            status=status.HTTP_200_OK,
            headers=headers
        )