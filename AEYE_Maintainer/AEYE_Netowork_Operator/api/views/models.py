from django.db import models

class aeye_mno_models (models.Model):
    whoami    = models.CharField(max_length=20)
    message   = models.CharField(max_length=20)
    operation = models.CharField(max_length=20)
    status    = models.CharField(max_length=20)

    def __str__(self):
        return self.name