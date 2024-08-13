from django.db import models

class aeye_inference_models (models.Model):
    whoami    = models.CharField(max_length=40)
    message   = models.CharField(max_length=40)
    image     = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class aeye_database_read_models (models.Model):
    whoami = models.CharField(max_length=40)
    message = models.CharField(max_length=40)
    request_data = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    

class aeye_database_write_models (models.Model):
    whoami = models.CharField(max_length=40)
    message = models.CharField(max_length=40)
    request_data = models.CharField(max_length=40)

    def __str__(self):
        return self.name