from django.db import models

class aeye_hal_print_log_models (models.Model):
    whoami             = models.CharField(max_length=20)
    message            = models.CharField(max_length=20)
    client_name_raw    = models.CharField(max_length=20)
    client_message_raw = models.CharField(max_length=20)
    client_status_raw  = models.CharField(max_length=20)


    def __str__(self):
        return self.name