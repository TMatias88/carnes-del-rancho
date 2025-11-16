from urllib.parse import quote_plus
from django.shortcuts import redirect, render
from cart.cart import CartService as Cart


def checkout(request):
    """
    Lee el carrito real, arma el mensaje con nombre, cantidad y precio,
    y redirige al WhatsApp de la carnicería.
    """
    cart = Cart(request)
    items = []
    total = 0

    # Recorremos el carrito real del CartService
    for item in cart:
        product = item.get("product")
        name = getattr(product, "name", "Producto sin nombre")
        qty = int(item.get("qty") or 1)  # ← CORREGIDO
        price = float(getattr(product, "price_crc", 0) or 0)  # ← CORREGIDO
        subtotal = price * qty
        total += subtotal
        items.append(f"* {qty} × {name} — ₡{int(subtotal):,}")

    # Si el carrito está vacío
    if not items:
        items.append("(Carrito vacío)")

    # Construcción del mensaje de WhatsApp
    lineas = [
        "Hola, quiero hacer un pedido desde la web:",
        *items,
        f"Total estimado: ₡{int(total):,}",
        "",
        "¿Me ayudan a coordinar el pago y la entrega? ",
    ]
    texto = quote_plus("\n".join(lineas))

    # Número real de WhatsApp de la carnicería
    wa_url = f"https://wa.me/50670381223?text={texto}"

    return redirect(wa_url)


def order_thanks(request):
    """
    Vista que muestra la página de agradecimiento luego del pedido.
    Debe existir la plantilla: templates/orders/thanks.html
    """
    return render(request, "orders/thanks.html")
