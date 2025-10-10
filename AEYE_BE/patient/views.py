from django.shortcuts import render
from .models import Patient, Patient_Image
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt



def get_all_patient(request):
    
    if request.method == 'GET':
        patients = Patient.objects.all().values()
        data = list(patients)
        
        return JsonResponse({"patients": data})


@csrf_exempt
def create_patient(request):

    if request.method == "POST":
        client_data=_parse_request_data(request)
        
        patient_name=client_data.get('name')
        patient_DOB=client_data.get('DOB')
        patient_sp=client_data.get('severity_percentage')
        patient_status=client_data.get('status')
        
        patient, created = Patient.objects.get_or_create(
            name=patient_name,
            DOB=patient_DOB,
            defaults={
                "severity_percentage": patient_sp,
                "status": patient_status,
            }
        )

        if created:
            message = "Succeeded to save patient."
        else:
            message = "Patient is already registered."

        return JsonResponse({"message": message})
                    
    return JsonResponse({"message": "Invalid request method."}, status=405)


def _parse_request_data(request):
    ct = (request.META.get("CONTENT_TYPE") or "").lower()

    if "application/json" in ct:
        try:
            body = request.body.decode(request.encoding or "utf-8")
            return json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")

    if "multipart/form-data" in ct or "application/x-www-form-urlencoded" in ct:
        return request.POST.dict()

    try:
        body = request.body.decode(request.encoding or "utf-8")
        return json.loads(body)
    except Exception:
        return request.POST.dict()