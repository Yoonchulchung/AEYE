from django.shortcuts import render
from .models import Checkup, AI_Diagnosis, OCT_Image
from django.http import JsonResponse


def ai_diagnose(request, id):
    return JsonResponse({"message" : "HI"})
