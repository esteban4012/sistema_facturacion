# muebleria/urls.py
from django.contrib import admin
from django.urls import path, include
from facturacion.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('facturacion.urls')),
]
