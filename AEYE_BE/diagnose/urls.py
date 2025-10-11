from rest_framework.routers import DefaultRouter

from .views import DiagnoseViewSet

app_name = 'dianose'

router = DefaultRouter()
router.register(r'', DiagnoseViewSet, basename='diagnose')

urlpatterns = router.urls