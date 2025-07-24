from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('usage', views.usage, name='usage'),
    path('contact', views.contact, name='contact')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
