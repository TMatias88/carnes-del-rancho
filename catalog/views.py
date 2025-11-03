from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def home(request):
    """
    Home con catálogo completo.
    """
    categories = Category.objects.all().order_by('name')
    products = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .order_by('name')
    )
    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "products": products,
            "current_category": None,   # útil para resaltar filtros
        },
    )

def catalog_view(request, category_slug=None):
    """
    Catálogo filtrado por categoría (opcional).
    - /catalogo/                -> todos los productos
    - /catalogo/<slug>/         -> productos de esa categoría
    """
    categories = Category.objects.all().order_by('name')
    products = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .order_by('name')
    )
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    return render(
        request,
        "home.html",  # reutilizamos la misma plantilla
        {
            "categories": categories,
            "products": products,
            "current_category": current_category,
        },
    )
