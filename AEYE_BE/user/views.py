from django.db import transaction
from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import User
from .serializers import UserReadSerializer, UserWriteSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return UserReadSerializer
        return UserWriteSerializer
    
    def retrieve(self, request, *args, **kwargs):
        '''
        특정 사용자를 조회합니다.
        '''
        
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
        
    def list(self, request, *args, **kwargs):
        '''
        모든 사용자를 조회합니다.
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
            "email": "test@test.com",
            "password": "1234qwer",
            "profile_image": "https://images.unsplash.com/..."
        }
        '''
        
        try:
            user_serializer = UserWriteSerializer(data=request.data)
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
        