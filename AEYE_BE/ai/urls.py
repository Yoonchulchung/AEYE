from rest_framework.routers import DefaultRouter

from .views import AIVersionViewSet

app_name = 'ai'

router = DefaultRouter()

router.register('', AIVersionViewSet, basename='AI Version')

urlpatterns = router.urls