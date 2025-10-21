from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DiagnosisViewSet

app_name = 'dianosis'

router = DefaultRouter()
router.register(r'', DiagnosisViewSet, basename='diagnosis')

urlpatterns = router.urls