# orders/forms.py
from django import forms

class CheckoutForm(forms.Form):
    nombre = forms.CharField(label="Nombre")
    telefono = forms.CharField(label="Teléfono")
    email = forms.EmailField(label="Correo")
    direccion = forms.CharField(label="Dirección de entrega", widget=forms.Textarea(attrs={"rows": 3}))
    # agrega aquí los demás campos que ya usas en tu checkout…

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            w = field.widget

            # Placeholder por label si no existe
            if "placeholder" not in w.attrs:
                w.attrs["placeholder"] = field.label

            # Aplica clases Bootstrap por tipo de widget (igual que el filtro add_class hacía)
            base = w.attrs.get("class", "").strip()

            if isinstance(w, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.PasswordInput, forms.URLInput, forms.Textarea)):
                w.attrs["class"] = (base + " form-control").strip()

            elif isinstance(w, (forms.Select, forms.SelectMultiple)):
                w.attrs["class"] = (base + " form-select").strip()

            elif isinstance(w, forms.CheckboxInput):
                w.attrs["class"] = (base + " form-check-input").strip()

            elif isinstance(w, forms.RadioSelect):
                # Bootstrap para radios en grupo
                w.attrs["class"] = (base + " form-check-input").strip()

            else:
                # fallback seguro
                w.attrs["class"] = (base + " form-control").strip()
