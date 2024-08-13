from django import forms
from .models import aeye_image_models

class aeye_image_form(forms.ModelForm):
    class Meta:
        model = aeye_image_models
        fields = ['image']
