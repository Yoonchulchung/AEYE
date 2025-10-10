from django.shortcuts import render
from .models import Patient, Patient_Image
from django.http import JsonResponse

def get_all_patient(request):
    
    if request.method == 'GET':
        patients = Patient.objects.all().values()
        data = list(patients)
        
        return JsonResponse({"patients": data})

        