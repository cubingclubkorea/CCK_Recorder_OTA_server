from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),  # 추가!
    path('list', views.list, name='list'),
    path('usage', views.usage, name='usage'),
    path('contact', views.contact, name='contact'),
    path('latest/<str:name>/', views.latest_firmware, name='latest_firmware'),
    path('download/<str:name>/', views.download_firmware, name='download_firmware'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
