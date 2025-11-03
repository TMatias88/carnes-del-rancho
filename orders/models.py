from django.db import models
from django.conf import settings

# Si tu modelo de producto está en catalog.models.Product:
from catalog.models import Product

class Order(models.Model):
    PAYMENT_CHOICES = [
        ("efectivo", "Efectivo"),
        ("sinpe", "SINPE"),
        ("tarjeta", "Tarjeta"),
    ]

    name = models.CharField("Nombre", max_length=120)
    phone = models.CharField("Teléfono", max_length=30, blank=True)
    email = models.EmailField("Correo", blank=True)
    payment_method = models.CharField("Método de pago", max_length=20, choices=PAYMENT_CHOICES, default="efectivo")
    receipt = models.FileField("Comprobante (opcional)", upload_to="receipts/", blank=True, null=True)

    total_crc = models.PositiveIntegerField("Total en CRC", default=0)

    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.name} - ₡{self.total_crc}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField("Cantidad", default=1)
    price_crc = models.PositiveIntegerField("Precio unidad CRC", default=0)
    total_crc = models.PositiveIntegerField("Total línea CRC", default=0)

    def __str__(self):
        return f"{self.qty} x {self.product.name} (₡{self.total_crc})"
