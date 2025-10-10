from django.db import models

class Patient(models.Model):
    
    class Status(models.TextChoices):
        MODERATE_RISK = 'MR', 'MODERATE_RISK'
        LOW_RISK = 'LR', 'LOW_RISK'
        HIGH_RISK = 'HR', 'HIGH_RISK'
        
    name = models.CharField(max_length=30)
    DOB = models.DateField()
    visit_nums = models.IntegerField()
    recent_visit_date = models.DateField()
    severity_percentage = models.IntegerField()
    status = models.CharField(
        max_length=2, 
        choices=Status.choices,
        default=Status.LOW_RISK,
    )
    db_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
class Patient_Image(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='patient_images/')
    db_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)