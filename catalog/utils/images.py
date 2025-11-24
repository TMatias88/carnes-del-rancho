# catalog/utils/images.py

from django.conf import settings

PLACEHOLDER = "/static/img/placeholder.png"

def resolve_image(product):
    """
    Devuelve SIEMPRE una URL válida de imagen.
    Prioridad:
    1. Imagen local (solo si realmente existe un archivo)
    2. URL RAW
    3. Placeholder
    """

    # 1. Imagen local (solo si el archivo realmente existe)
    if getattr(product, "image_file", None) and product.image_file.name:
        try:
            return product.image_file.url
        except:
            pass

    # 2. URL RAW (GitHub RAW o DigitalOcean URL)
    if getattr(product, "image_url", None):
        return product.image_url

    # 3. Placeholder
    return PLACEHOLDER
