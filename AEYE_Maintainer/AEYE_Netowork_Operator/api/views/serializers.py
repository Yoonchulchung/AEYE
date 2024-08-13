from rest_framework import serializers
from .models import aeye_mno_models


class aeye_mno_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_mno_models
        fields = ['whoami', 'message', 'operation', 'status']
