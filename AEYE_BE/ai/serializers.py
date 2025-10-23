from rest_framework import serializers

from .models import AIVersion


class AIVersionSerializer(serializers.ModelSerializer):
    '''
    
    Response Body: 
    "ai_version": {
          "oct_model_name": "OCT 모델 이름",
          "oct_model_weight": "OCT 모델에 사용된 가중치 이름",
          "oct_probability": "OCT 모델 정확도",
          "oct_version": "OCT 모델 버젼",
          "llm_model_name": "llm 모델 이름",
          "llm_model_weight": "llm 모델 가중치 이름",
      }
    '''
    
    class Meta:
        model = AIVersion
        fields = ["oct_model_name", "oct_model_weight", "oct_probability", 
                  "oct_version", "llm_model_name", "llm_model_weight"]