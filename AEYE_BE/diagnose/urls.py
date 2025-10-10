from django.urls import path
from . import views

app_name = 'dianose'

urlpatterns = [
    path("<int:id>/", views.ai_diagnose, name="ai_diagnose"),
]