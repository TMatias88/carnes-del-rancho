import os
from django.core.management.base import BaseCommand
from catalog.models import Product

class Command(BaseCommand):
    help = "Reasigna imágenes desde Spaces usando exactamente el nombre original."

    def handle(self, *args, **kwargs):
        base_url = "products/"  # Carpeta donde subiste las imágenes en DO

        productos = Product.objects.all()
        total = productos.count()
        self.stdout.write(f"Iniciando proceso para {total} productos...\n")

        for p in productos:
            if not p.image:
                self.stdout.write(f"⚠ Producto sin imagen asignada en BD: {p.name}")
                continue

            # Nombre actual guardado en Django
            filename = os.path.basename(p.image.name)

            # Construir nombre correcto para Spaces
            correcto = f"{base_url}{filename}"

            # Asignar al campo image, NO sube nada, solo actualiza la ruta
            p.image.name = correcto
            p.save(update_fields=["image"])

            self.stdout.write(f"✓ {p.name} -> {correcto}")

        self.stdout.write("\n🎉 Listo. Imágenes reasignadas correctamente.\n")








