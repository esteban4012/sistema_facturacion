# # facturacion/serializers.py
# from rest_framework import serializers
# from .models import Factura, Articulo

# class ArticuloSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Articulo
#         fields = '__all__'

# class FacturaSerializer(serializers.ModelSerializer):
#     articulos = ArticuloSerializer(many=True)

#     class Meta:
#         model = Factura
#         fields = '__all__'

# facturacion/serializers.py
from rest_framework import serializers
from .models import Factura, Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    articulos = ArticuloSerializer(many=True)

    class Meta:
        model = Factura
        fields = '__all__'

    def create(self, validated_data):
        articulos_data = validated_data.pop('articulos')
        factura = Factura.objects.create(**validated_data)
        for articulo_data in articulos_data:
            Articulo.objects.create(factura=factura, **articulo_data)
        return factura

    def update(self, instance, validated_data):
        articulos_data = validated_data.pop('articulos')
        articulos = instance.articulos.all()
        articulos = list(articulos)
        
        instance.nombre_cliente = validated_data.get('nombre_cliente', instance.nombre_cliente)
        instance.cedula = validated_data.get('cedula', instance.cedula)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.valor_total = validated_data.get('valor_total', instance.valor_total)
        instance.save()

        for articulo_data in articulos_data:
            articulo = articulos.pop(0)
            articulo.descripcion = articulo_data.get('descripcion', articulo.descripcion)
            articulo.cantidad = articulo_data.get('cantidad', articulo.cantidad)
            articulo.valor = articulo_data.get('valor', articulo.valor)
            articulo.save()

        return instance

