from django.db import models

from patient.models import Patient
from utils.common_models import CommonModel


class Checkup(CommonModel):
    
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='checkup', db_index=True
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Checkup({self.patient.name}, {self.date})"

class OCTImage(CommonModel):
    checkup = models.ForeignKey(
        Checkup,
        on_delete=models.SET_NULL,
        related_name='oct_image',
        null=True,
    )
    oct_img = models.ImageField(upload_to='patient_oct_images/')
    
    def __str__(self):
        return f"OCT Image({self.image})"
    
class CheckupMeta(CommonModel):
    
    class Eye_Side(models.TextChoices):
        LEFT  = 'L', 'LEFT'
        RIGHT = 'R', 'RIGHT'
    
    checkup = models.ForeignKey(
        Checkup, on_delete=models.CASCADE, related_name='meta', db_index=True
    )
    eye_side = models.CharField(max_length=1, choices=Eye_Side, db_index=True)
    
    def __str__(self):
        return f"{self.checkup.patient.name}, {self.eye_side}"
    
class Diagnosis(CommonModel):
    
    class Status(models.TextChoices):
        MODERATE_RISK = 'MR', 'MODERATE_RISK'
        LOW_RISK = 'LR', 'LOW_RISK'
        HIGH_RISK = 'HR', 'HIGH_RISK'

    class Kind(models.TextChoices):
        DOCTOR = 'DR', 'DOCTOR'
        AI     = 'AI', 'AI'
        REVIEW = 'RV', 'REVIEW'
    
    checkup = models.ForeignKey(
        Checkup, on_delete=models.CASCADE, related_name='diagnosis', db_index=True
    )
    date   = models.DateTimeField(auto_now=True)
    kind   = models.CharField(max_length=2, choices=Kind.choices, db_index=True)
    status = models.CharField(max_length=2, choices=Status.choices, db_index=True)
    classification = models.TextField(blank=True)
    result = models.CharField(max_length=2048, blank=True)
    result_summary = models.CharField(max_length=2048, blank=True)
    
    def __str__(self):
        return f"Diagnosis({self.checkup.patient.name}, {self.kind}, {self.result})"