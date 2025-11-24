# catalog/utils/images.py

from django.conf import settings

PLACEHOLDER = "/static/img/placeholder.png"
def resolve_image(product):
    # 1. Imagen local (solo si de verdad EXISTE un archivo en media/)
    if product.image_file and product.image_file.name and product.image_file.storage.exists(product.image_file.name):
        return product.image_file.url

    # 2. URL RAW
    if product.image_url:
        return product.image_url

    return "/static/img/placeholder.png"

