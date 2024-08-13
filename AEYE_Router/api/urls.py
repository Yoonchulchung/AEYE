from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views.AEYE_WNO import aeye_wno_Viewsets

router = DefaultRouter()

router.register(r'web-network-operator', aeye_wno_Viewsets)


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

