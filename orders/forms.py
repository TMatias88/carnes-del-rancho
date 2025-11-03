from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "email", "payment_method", "receipt"]
        labels = {
            "name": "Nombre completo",
            "phone": "Teléfono",
            "email": "Correo",
            "payment_method": "Método de pago",
            "receipt": "Comprobante (opcional, para SINPE)",
        }
        widgets = {
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }
