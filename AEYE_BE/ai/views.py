from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from .serializers import AIVersionSerializer
from .models import AIVersion
from rest_framework.response import Response


class AIVersionViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    
    queryset=AIVersion.objects.all()
    serializer_class = AIVersionSerializer

    def list(self, request, *args, **kwargs):
        '''
        모든 AI 모델 정보를 조회합니다.
        '''
        
        qs = self.get_queryset()
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)
    
    @transaction.atomic
    def create(self, request, args, **kwargs):
        '''
        새로운 AI 모델 정보를 입력합니다.
        
        Request Body:
        {
            "oct_model_name": "OCT 모델 이름",
            "oct_model_weight": "OCT 모델에 사용된 가중치 이름",
            "oct_probability": "OCT 모델 정확도",
            "oct_version": "OCT 모델 버젼",
            "llm_model_name": "llm 모델 이름",
            "llm_model_weight": "llm 모델 가중치 이름",
        }
        '''
        
        try:
            user_serializer = AIVersionSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            
            payload = {
                "status" : "SUCCESS"
            }
        except Exception as e:
            payload = {
                "status" : "ERROR",
                "message" : str(e),
            }

        return Response(data=payload, status=status.HTTP_202_ACCEPTED)