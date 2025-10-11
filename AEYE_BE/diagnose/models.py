from django.db import models

from patient.models import Patient
from utils.common_models import CommonModel


class Checkup(CommonModel):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='checkups', db_index=True
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Checkup({self.patient}, {self.date})"


class OCTImage(CommonModel):
    checkup_id = models.ForeignKey(
        Checkup,
        on_delete=models.SET_NULL,
        related_name='oct_images',
        null=True,
    )
    image = models.ImageField(upload_to='patient_oct_images/')
    
    
class DiagnosisInfo(CommonModel):
    
    class Status(models.TextChoices):
        MODERATE_RISK = 'MR', 'MODERATE_RISK'
        LOW_RISK = 'LR', 'LOW_RISK'
        HIGH_RISK = 'HR', 'HIGH_RISK'

    class Kind(models.TextChoices):
        DOCTOR = 'DR', 'DOCTOR'
        AI     = 'AI', 'AI'
        REVIEW = 'RV', 'REVIEW'

    checkup = models.ForeignKey(
        Checkup, on_delete=models.CASCADE, related_name='diagnoses', db_index=True
    )
    kind   = models.CharField(max_length=2, choices=Kind.choices, db_index=True)
    status = models.CharField(max_length=2, choices=Status.choices, db_index=True)
    result = models.CharField(max_length=255, blank=True)
    classification = models.TextField(blank=True)