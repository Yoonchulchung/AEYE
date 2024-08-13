from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views.AEYE_Print_log import aeye_print_log_Viewswets

router = DefaultRouter()

router.register(r'print-log', aeye_print_log_Viewswets)


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

