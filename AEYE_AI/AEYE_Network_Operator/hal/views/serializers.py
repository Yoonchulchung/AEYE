from rest_framework import serializers
from .models import aeye_print_log_models

class aeye_print_log_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_print_log_models
        fields = ['whoami', 'message']
