from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views.AEYE_ANO import aeye_ano_Viewsets

router = DefaultRouter()

router.register(r'ai-network-operator', aeye_ano_Viewsets)


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

