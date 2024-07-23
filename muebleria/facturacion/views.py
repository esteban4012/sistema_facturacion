
from django.utils import timezone
from rest_framework import viewsets
from .models import Factura, Articulo
from .serializers import FacturaSerializer
from django.forms import inlineformset_factory
from .forms import FacturaForm, ArticuloForm, FacturaSearchForm

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

# facturacion/views.py
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FacturaForm, ArticuloFormSet


def home(request):
    return render(request, 'facturacion/home.html')


def crear_factura(request):
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.fecha = timezone.now()
            factura.save()

            # Procesar artículos
            articulos_data = []
            total_valor = 0
            index = 0
            while f'articulos-{index}-descripcion' in request.POST:
                descripcion = request.POST[f'articulos-{index}-descripcion']
                cantidad = int(request.POST[f'articulos-{index}-cantidad'])
                valor_unitario = float(request.POST[f'articulos-{index}-valor'])
                valor_total = cantidad * valor_unitario
                total_valor += valor_total
                articulo = Articulo(
                    factura=factura, 
                    descripcion=descripcion, 
                    cantidad=cantidad, 
                    valor=valor_unitario, 
                    valor_total=valor_total
                )
                articulos_data.append(articulo)
                index += 1

            # Guardar artículos y actualizar el valor total de la factura
            Articulo.objects.bulk_create(articulos_data)
            factura.valor_total = total_valor
            factura.save()

            return redirect('lista_facturas')
    else:
        form = FacturaForm(initial={'fecha': timezone.now()})

    return render(request, 'facturacion/crear_factura.html', {'form': form})


def lista_facturas(request):
    search_form = FacturaSearchForm(request.GET or None)
    facturas = Factura.objects.all()

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            facturas = facturas.filter(nombre_cliente__icontains=search_query) | facturas.filter(cedula__icontains=search_query)

    return render(request, 'facturacion/lista_facturas.html', {
        'facturas': facturas,
        'search_form': search_form,
    })

def ver_factura(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    return render(request, 'facturacion/ver_factura.html', {'factura': factura})


def editar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        formset = ArticuloFormSet(request.POST, instance=factura)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('lista_facturas')
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = FacturaForm(instance=factura)
        formset = ArticuloFormSet(instance=factura)
    return render(request, 'facturacion/editar_factura.html', {'form': form, 'formset': formset, 'factura': factura})

def ver_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    articulos = Articulo.objects.filter(factura=factura) 
    return render(request, 'facturacion/ver_factura.html', {'factura': factura, 'articulos': articulos})


def eliminar_factura(request, factura_id):
    factura = get_object_or_404(Factura, pk=factura_id)
    factura.delete()
    return redirect('lista_facturas')