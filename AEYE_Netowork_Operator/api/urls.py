from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views.AEYE_MNO import aeye_mno_Viewsets

router = DefaultRouter()

router.register(r'maintainer-network-operator', aeye_mno_Viewsets)



urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

