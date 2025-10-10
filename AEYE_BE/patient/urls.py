from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path("", views.get_all_patient, name="get_all_patient"),
]