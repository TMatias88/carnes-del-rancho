from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from catalog.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm

def _get_cart_items_from_session(request):
    """
    Lee el carrito desde la sesión y arma:
    - items: lista de dicts con producto, qty, price_crc, total
    - total_crc: suma de todos
    Estructura esperada en session:
      cart = { "<product_id>": {"qty": int, "price_crc": int}, ... }
    """
    cart = request.session.get("cart", {}) or {}
    items = []
    total_crc = 0

    for pid_str, data in cart.items():
        try:
            pid = int(pid_str)
        except ValueError:
            continue

        qty = int(data.get("qty", 1))
        price_crc = int(data.get("price_crc", 0))

        try:
            product = Product.objects.get(id=pid)
        except ObjectDoesNotExist:
            # Si el producto ya no existe, saltamos esta línea
            continue

        line_total = price_crc * qty
        total_crc += line_total

        items.append({
            "product": product,
            "qty": qty,
            "price_crc": price_crc,
            "total": line_total,
        })

    summary = {"total_crc": total_crc}
    return items, summary


def checkout(request):
    # Construye items/summary siempre (GET y POST) para que el template tenga datos
    items, summary = _get_cart_items_from_session(request)

    # Si no hay items en el carrito, no tiene sentido seguir
    if not items:
        messages.info(request, "Tu carrito está vacío. Agrega productos antes de continuar al checkout.")
        return redirect("home")

    if request.method == "POST":
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.total_crc = summary["total_crc"]
                order.save()

                # Crear las líneas del pedido
                for it in items:
                    OrderItem.objects.create(
                        order=order,
                        product=it["product"],
                        qty=it["qty"],
                        price_crc=it["price_crc"],
                        total_crc=it["total"],
                    )

                # Vaciar el carrito
                request.session["cart"] = {}
                request.session.modified = True

            messages.success(request, "¡Pedido confirmado! Gracias por su compra.")
            return redirect("orders:order_thanks")
        else:
            messages.error(request, "Por favor revisa los datos del formulario.")
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {
        "items": items,
        "summary": summary,
        "form": form,
    })


def order_thanks(request):
    return render(request, "order_thanks.html")
