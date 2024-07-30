from django.db import models

# Create your models here.

class UploadedImage(models.Model):
    # 저장 경로: MEDIA_ROOT/uploaded_images/xxx.png
    image = models.ImageField(blank=True, upload_to='uploaded_images')
