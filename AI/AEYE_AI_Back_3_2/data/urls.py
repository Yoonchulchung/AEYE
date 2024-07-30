from django.urls import path
from .views import ReceiveImageView

urlpatterns = [
    path('receive-image', ReceiveImageView.as_view(), name='receive-image'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)