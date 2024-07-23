# facturacion/urls.py
from django.urls import path
from .views import crear_factura, lista_facturas, ver_factura, editar_factura, eliminar_factura

urlpatterns = [
    path('crear_factura/', crear_factura, name='crear_factura'),
    path('lista_facturas/', lista_facturas, name='lista_facturas'),
    path('editar_factura/<int:factura_id>/', editar_factura, name='editar_factura'),
    path('factura/<int:id>/',ver_factura, name='ver_factura'),
    path('eliminar_factura/<int:factura_id>/', eliminar_factura, name='eliminar_factura'),
]
