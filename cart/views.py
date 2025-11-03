from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from catalog.models import Product
from .cart import CartService
from django.template.loader import render_to_string
from django.http import JsonResponse

def cart_view(request):
    cart = CartService(request)
    items = list(iter(cart))
    summary = cart.summary()
    return render(request, "cart.html", {"items": items, "summary": summary})

@require_POST
def add_to_cart(request, product_id):
    qty = int(request.POST.get("qty", 1))
    # Si tu modelo NO tiene is_active, quita el filtro:
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = CartService(request)
    cart.add(product.id, qty=qty)
    request.session.modified = True
    messages.success(request, f"“{getattr(product, 'name', 'Producto')}” agregado al carrito.")
    return redirect("cart:cart_view")

@require_POST
def remove_item(request, product_id):
    cart = CartService(request)
    cart.remove(product_id)
    request.session.modified = True
    messages.info(request, "Producto removido del carrito.")
    return redirect("cart:cart_view")

@require_POST
def clear_cart(request):
    cart = CartService(request)
    cart.clear()
    request.session.modified = True
    messages.info(request, "Carrito vaciado.")
    return redirect("cart:cart_view")


def cart_panel(request):
    cart = CartService(request)
    items = list(iter(cart))
    summary = cart.summary()
    # Si lo piden por fetch/AJAX, devuelvo HTML parcial
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("cart/_panel.html", {"items": items, "summary": summary}, request=request)
        return JsonResponse({"html": html})
    # fallback: render normal
    return render(request, "cart/_panel.html", {"items": items, "summary": summary})
