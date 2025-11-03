import json
from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Payment
from .gateways import placetopay

# Si ya tenés Order:
# from orders.models import Order
# y reemplazás donde usamos session/email/total

def iniciar_pago(request, order_number: str):
    """
    1) Obtener total/email (de tu Order o del carrito en sesión).
    2) Crear sesión en gateway y redirigir al checkout BAC.
    """
    # ---- Si ya tenés Order real, usá esto: ----
    # order = get_object_or_404(Order, number=order_number, status="pending")
    # total_crc = order.total_crc
    # email = order.customer_email

    # ---- Mientras tanto, usamos sesión como ejemplo: ----
    total_crc = request.session.get("checkout_total_crc")
    email = request.session.get("checkout_email") or ""

    if not total_crc:
        return HttpResponseBadRequest("No hay total para procesar el pago.")

    resp = placetopay.create_session(
        order_number=order_number,
        total_crc=str(total_crc),
        description=f"Orden {order_number}",
        email=email,
    )
    process_url = resp.get("processUrl")
    request_id  = str(resp.get("requestId"))

    Payment.objects.update_or_create(
        order_number=order_number,
        defaults={
            "gateway": "placetopay",
            "request_id": request_id,
            "process_url": process_url,
            "raw": resp,
            "status": "created",
        }
    )
    return redirect(process_url)

def _actualizar_estado(order_number: str, request_id: str):
    data = placetopay.query_session(request_id)
    status = (data.get("status") or {}).get("status") or "unknown"
    pay = Payment.objects.filter(order_number=order_number, request_id=request_id).first()
    if pay:
        pay.status, pay.raw = status, data
        pay.save()

    # Si tenés Order, podés setear paid/failed:
    # order = Order.objects.filter(number=order_number).first()
    # if order:
    #     if status in ("APPROVED", "OK", "APPROVED_PARTIAL"):
    #         order.status = "paid"
    #     elif status in ("REJECTED", "FAILED"):
    #         order.status = "failed"
    #     order.save()

    return status, data

def retorno_pago(request):
    order_number = request.GET.get("order")
    if not order_number:
        return HttpResponseBadRequest("Falta order.")
    pay = get_object_or_404(Payment, order_number=order_number)
    _actualizar_estado(order_number, pay.request_id)
    return render(request, "payments/resultado.html", {"order_number": order_number, "pago": pay})

@csrf_exempt
def webhook_pago(request):
    try:
        payload = json.loads(request.body.decode() or "{}")
    except Exception:
        payload = {}
    req_id = str(payload.get("requestId") or "")
    ref    = str(payload.get("reference") or payload.get("order") or "")
    if req_id:
        pay = Payment.objects.filter(request_id=req_id).first()
        order_number = ref or (pay.order_number if pay else "")
        if order_number:
            _actualizar_estado(order_number, req_id)
    return HttpResponse("ok")
