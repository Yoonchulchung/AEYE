from django.urls import path
from rest_framework.routers import DefaultRouter

from diagnosis.api.ai import DiagnosisAIViewSet

app_name = 'dianosis'

router = DefaultRouter()
router.register(r'', DiagnosisAIViewSet, basename='diagnosis')

urlpatterns = router.urls