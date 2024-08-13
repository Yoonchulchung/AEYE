from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views.AEYE_Inference import aeye_inference_Viewswets
from .views.AEYE_Train import aeye_train_Viewswets
from .views.AEYE_Test import aeye_test_Viewswets
from .views.AEYE_PtM import aeye_ptm_Viewswets

router = DefaultRouter()

router.register(r'ai-inference', aeye_inference_Viewswets)
router.register(r'ai-train', aeye_train_Viewswets)
router.register(r'ai-test', aeye_test_Viewswets)
router.register(r'print-to-maintainer', aeye_ptm_Viewswets)


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

