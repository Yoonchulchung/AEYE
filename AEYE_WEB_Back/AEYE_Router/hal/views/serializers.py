from rest_framework import serializers
from .models import aeye_inference_models, aeye_database_read_models, aeye_database_write_models

class aeye_inference_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_inference_models
        fields = ['whoami', 'image', 'message']


class aeye_database_read_serializers(serializers.ModelSerializer):

    class Meta:
        model = aeye_database_read_models
        fields = ['whoami', 'message', 'request_data']


class aeye_database_write_serializers(serializers.ModelSerializer):

    class Meta:
        model = aeye_database_write_models
        fields = ['whoami', 'message', 'request_data']

