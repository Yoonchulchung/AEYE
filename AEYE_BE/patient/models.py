from django.db import models

class Patient(models.Model):
    
    class Status(models.TextChoices):
        MODERATE_RISK = 'MR', 'MODERATE_RISK'
        LOW_RISK = 'LR', 'LOW_RISK'
        HIGH_RISK = 'HR', 'HIGH_RISK'
        
    name = models.CharField(max_length=30)
    DOB = models.DateField()
    visit_nums = models.IntegerField(default=1)
    recent_visit_date = models.DateField(auto_now_add=True)
    severity_percentage = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=2, 
        choices=Status.choices,
        default=Status.LOW_RISK,
        null=True,
        blank=True
    )
    db_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)