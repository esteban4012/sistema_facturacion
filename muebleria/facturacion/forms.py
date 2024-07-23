from django import forms
from django.forms import inlineformset_factory
from .models import Factura, Articulo

# class FacturaForm(forms.ModelForm):
#     class Meta:
#         model = Factura
#         fields = ['nombre_cliente', 'cedula', 'direccion', 'valor_total', 'pagado']
#         widgets = {
#             'fecha': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
#         }

# class ArticuloForm(forms.ModelForm):
#     class Meta:
#         model = Articulo
#         fields = ['descripcion', 'cantidad', 'valor']

# ArticuloFormSet = inlineformset_factory(Factura, Articulo, form=ArticuloForm, extra=1, can_delete=True)

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [ 'nombre_cliente', 'direccion', 'cedula', 'valor_total', 'pagado']

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['descripcion', 'cantidad', 'valor', 'valor_total']

ArticuloFormSet = inlineformset_factory(Factura, Articulo, form=ArticuloForm, extra=1)

class FacturaSearchForm(forms.Form):
    search_query = forms.CharField(label='Buscar por nombre del cliente o cédula', max_length=100, required=False)
