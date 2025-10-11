from rest_framework import serializers

from .models import AIVersion


class AIVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIVersion
        fields = ["model_name", "model_weight", "version", "ai_probability"]