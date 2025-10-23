from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from diagnosis.models import Diagnosis
from utils.common_models import CommonModel


class AIVersion(CommonModel):
    
    diagnosis = models.OneToOneField(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name='ai_version'
    )
    oct_model_name     = models.CharField(max_length=10)
    oct_model_weight   = models.CharField(max_length=30)
    oct_probability = models.PositiveSmallIntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)],
            null=True, blank=True
        )
    oct_version        = models.CharField(max_length=10)
    
    llm_model_name = models.CharField(max_length=10)
    llm_model_weight = models.CharField(max_length=30)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.diagnosis and self.diagnosis.kind != Diagnosis.Kind.AI:
            raise ValidationError("AIVersion은 diagnosis.kind가 AI일 때만 생성할 수 있습니다.")
        
    def __str__(self):
        return f"{self.oct_model_name} v{self.version}, {self.llm_model_name}"