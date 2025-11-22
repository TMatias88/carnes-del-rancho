# catalog/utils/images.py

from django.conf import settings

PLACEHOLDER = "/static/img/placeholder.png"

def resolve_image(product):
    """
    Devuelve SIEMPRE una URL válida de imagen.
    Prioridad:
    1. Imagen local (solo desarrollo)
    2. URL RAW (producción)
    3. Placeholder
    """

    # 1. Imagen local (solo desarrollo)
    if getattr(product, "image_file", None):
        try:
            return product.image_file.url
        except:
            pass

    # 2. URL RAW (GitHub / DO)
    if getattr(product, "image_url", None):
        return product.image_url

    # 3. Placeholder
    return PLACEHOLDER
