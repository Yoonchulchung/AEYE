from django.db import models

class aeye_inference_models (models.Model):
    whoami    = models.CharField(max_length=20)
    message   = models.CharField(max_length=20)
    image     = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class aeye_image_models(models.Model):
    image = models.ImageField(upload_to='images/')

class aeye_train_models (models.Model):
    whoami    = models.CharField(max_length=20)
    message   = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class aeye_test_models (models.Model):
    whoami    = models.CharField(max_length=20)
    message   = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class aeye_ptm_models (models.Model):
    whoami    = models.CharField(max_length=20)
    message   = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name