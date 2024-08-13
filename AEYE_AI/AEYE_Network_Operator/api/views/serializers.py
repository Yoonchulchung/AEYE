from rest_framework import serializers
from .models import aeye_ano_models

class aeye_ano_serializers(serializers.ModelSerializer):
    
    image = serializers.ImageField(required=False)

    class Meta:
        model = aeye_ano_models
        fields = ['whoami', 'message', 'image', 'operation']
