from django.urls import path
from rest_framework.routers import DefaultRouter

from .api.ai import DiagnosisAIViewSet

app_name = 'dianosis'

#router = DefaultRouter()
#router.register(r'', DiagnosisAIViewSet, basename='diagnosis')

urlpatterns = [
               path('', DiagnosisAIViewSet.as_view(), name='diagnosis'),]