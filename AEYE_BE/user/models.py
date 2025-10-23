from django.db import models

from utils.common_models import CommonModel


class User(CommonModel):
    
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='user_image/')