# facturacion/admin.py
from django.contrib import admin
from .models import Factura, Articulo

class ArticuloInline(admin.TabularInline):
    model = Articulo
    extra = 1  # Número de formularios en blanco adicionales

class FacturaAdmin(admin.ModelAdmin):
    inlines = [ArticuloInline,]

admin.site.register(Factura, FacturaAdmin)


