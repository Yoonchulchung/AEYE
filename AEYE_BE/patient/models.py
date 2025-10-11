from django.db import models

from utils.common_models import CommonModel


class Patient(CommonModel):
    
    name = models.CharField(max_length=30)
    DOB = models.DateField()
    visit_nums = models.IntegerField(default=1)
    recent_visit_date = models.DateField(auto_now_add=True)