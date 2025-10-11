from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from diagnose.models import DiagnosisInfo
from utils.common_models import CommonModel


class AIVersion(CommonModel):
    
    diagnosis = models.OneToOneField(
        DiagnosisInfo,
        on_delete=models.CASCADE,
        related_name='ai_version'
    )
    model_name     = models.CharField(max_length=10)
    model_weight   = models.CharField(max_length=30)
    version        = models.CharField(max_length=10)
    ai_probability = models.PositiveSmallIntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)],
            null=True, blank=True
        )
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.diagnosis and self.diagnosis.kind != DiagnosisInfo.Kind.AI:
            raise ValidationError("AIVersion은 diagnosis.kind가 AI일 때만 생성할 수 있습니다.")
        
    def __str__(self):
        return f"{self.model_name} v{self.version} for Dx {self.diagnosis_id}"