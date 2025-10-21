from django.contrib import admin

from .models import Checkup, DiagnosisInfo


@admin.register(Checkup)
class CheckupAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'date']
    search_fields = ['patient__name']
    
    def patient_name(self, obj):
        return obj.patient.name

@admin.register(DiagnosisInfo)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['checkup_patient_name', 'checkup', 'kind', 'status', 'result', 'classification']
    search_fields = ['checkup']
    
    def checkup_patient_name(self, obj):
        return obj.checkup.patient.name