from rest_framework import serializers

from .models import AIVersion

class AIVersionSerializer(serializers.ModelSerializer):
    '''
    
    Response Body: 
    "ai_version": {
          "model_name": "AI 모델 이름",
          "model_weight": "AI에 사용된 가중치 이름",
          "probability": "AI 모델 정확도",
          "version": "AI 모델 버젼",
      }
    '''
    
    class Meta:
        model = AIVersion
        fields = ["model_name", "model_weight", "version", "ai_probability"]