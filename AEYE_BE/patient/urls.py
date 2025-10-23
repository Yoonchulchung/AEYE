from rest_framework.routers import DefaultRouter

from .views import PatientViewSet

app_name = 'patient'

router = DefaultRouter()

router.register('', PatientViewSet, basename=["patient"])
urlpatterns = router.urls