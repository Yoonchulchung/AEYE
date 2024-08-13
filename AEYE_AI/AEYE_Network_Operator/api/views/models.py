from django.db import models

class aeye_ano_models (models.Model):
    whoami    = models.CharField(max_length=20)
    message   = models.CharField(max_length=20)
    image     = models.ImageField(upload_to='images/')
    operation = models.CharField(max_length=20)

    def __str__(self):
        return self.name
