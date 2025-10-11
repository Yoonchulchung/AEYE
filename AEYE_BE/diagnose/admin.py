from django.contrib import admin
from .models import DiagnosisInfo, Checkup

@admin.register(Checkup)
class CheckupAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date']
    search_fields = ['patient']

@admin.register(DiagnosisInfo)
class DiagnoseAdmin(admin.ModelAdmin):
    list_display = ['checkup', 'kind', 'status', 'result', 'classification']
    search_fields = ['checkup']