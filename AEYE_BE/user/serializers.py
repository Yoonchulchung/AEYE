from rest_framework import serializers
from .models import User

class UserReadSerializer(serializers.ModelSerializer):
    '''
    
    Response Body:
    {
        "user_id": 1,
        "email": "test@test.com",
        "password": "1234qwer",
        "profile_image": "https://images.unsplash.com/..."
    }
    '''
    
    user_id = serializers.IntegerField(source="id")
    
    class Meta:
        model = User
        fields = ["user_id", "email", "password", "profile_image"]
        
class UserWriteSerializer(serializers.ModelSerializer):
    '''
    
    Response Body:
    {
        "email": "test@test.com",
        "password": "1234qwer",
        "profile_image": "https://images.unsplash.com/..."
    }
    '''

    class Meta:
        model = User
        fields = ["email", "password", "profile_image"]