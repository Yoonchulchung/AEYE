from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views.AEYE_Inference import aeye_inference_Viewswets
from .views.AEYE_DataBase_Write import aeye_database_write_Viewswets
from .views.AEYE_DataBase_Read  import aeye_database_read_Viewswets

router = DefaultRouter()


router.register(r'ai-inference', aeye_inference_Viewswets)
router.register(r'database-write', aeye_database_write_Viewswets)
router.register(r'database-read', aeye_database_read_Viewswets)


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

