from django.db import models
from patient.models import Patient

    
class AI_Diagnosis(models.Model):
    ai_probability = models.IntegerField()
    result = models.CharField(max_length=255)
    db_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
class Checkup(models.Model):
    
    class Status(models.TextChoices):
        MODERATE_RISK = 'MR', 'MODERATE_RISK'
        LOW_RISK = 'LR', 'LOW_RISK'
        HIGH_RISK = 'HR', 'HIGH_RISK'
        
    patient_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE,
        related_name='checkups',
    )
    date = models.DateField(auto_now_add=True)
    sytmptom = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
    )
    ai_diagnosis = models.ForeignKey(
        AI_Diagnosis,
        on_delete=models.SET_NULL,
        related_name='checkups',
        null=True,
    )
    doctor_diagnosis = models.CharField(max_length=255, null=True)
    db_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    

class OCT_Image(models.Model):
    checkup_id = models.ForeignKey(
        Checkup,
        on_delete=models.SET_NULL,
        related_name='oct_image',
        null=True
    )
    image = models.ImageField(upload_to='patient_oct_images/')
    db_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)