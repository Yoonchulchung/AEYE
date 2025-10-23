from django.urls import path
from rest_framework.routers import DefaultRouter

from diagnosis.api.ai import DiagnosisAIViewSet
from diagnosis.api.doctor import DiagnosisDoctorViewSet

app_name = 'dianosis'

router = DefaultRouter()
router.register(r'ai', DiagnosisAIViewSet, basename='diagnosis AI')
router.register(r'doctor', DiagnosisDoctorViewSet, basename='diagnosis Doctor')

urlpatterns = router.urls