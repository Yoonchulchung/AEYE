from rest_framework import serializers
from .models import aeye_hal_print_log_models


class aeye_hal_print_log_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_hal_print_log_models
        fields = ['whoami', 'message', 'client_name_raw', 'client_message_raw', 'client_status_raw']
