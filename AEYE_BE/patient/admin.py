from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'DOB', 'visit_nums']
    search_fields = ['name']