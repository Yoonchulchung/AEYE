from django.db import models

from utils.common_models import CommonModel


class Patient(CommonModel):
    
    name = models.CharField(max_length=30)
    DOB = models.DateField()
    profile_image = models.ImageField(upload_to='patient_image/')
    visit_nums = models.IntegerField(default=1)
    recent_visit = models.DateField(auto_now_add=True)
    severity_percentage = models.IntegerField(default=0)
    
    class Status(models.TextChoices):
        MODERATE_RISK = 'MR', 'MODERATE_RISK'
        LOW_RISK = 'LR', 'LOW_RISK'
        HIGH_RISK = 'HR', 'HIGH_RISK'
        
    status = models.CharField(max_length=2, choices=Status.choices, db_index=True, blank=True, null=True)
    
    def __str__(self):
        return f"Patient({self.name}, {self.DOB}, {self.visit_nums}, {self.recent_visit})"