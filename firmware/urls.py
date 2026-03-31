from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('list', views.list, name='list'),
    path('usage', views.usage, name='usage'),
    path('contact', views.contact, name='contact'),
    path('device/login', views.DeviceTokenView.as_view(), name='device_login'),
    path('device/download', views.ProtectedFirmwareDownload.as_view(), name='download_firmware'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
