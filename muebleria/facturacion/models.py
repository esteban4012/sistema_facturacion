from django.db import models

class Factura(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    fecha = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda primero la factura para obtener su ID

        # Recalcular el valor total de la factura
        self.valor_total = sum(articulo.valor_total for articulo in self.articulos.all())
        super().save(*args, **kwargs)  # Guarda nuevamente para actualizar el valor_total

    def __str__(self):
        return f"Factura {self.id} - {self.nombre_cliente}"

class Articulo(models.Model):
    factura = models.ForeignKey(Factura, related_name='articulos', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.valor_total = self.cantidad * self.valor
        super().save(*args, **kwargs)
        # Update factura total value
        self.factura.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Update factura total value after deletion
        self.factura.save()

    def __str__(self):
        return self.descripcion
