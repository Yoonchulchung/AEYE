from django.contrib import admin
from .models import Patient, Patient_Image

admin.site.register(Patient_Image)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'DOB', 'visit_nums', 'status', 'severity_percentage']
    search_fields = ['name']