import unicodedata

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from catalog.models import Product, Category

# Si tienes un modelo para guardar mensajes en admin:
try:
    from .models import ContactMessage  # name, phone, email, [subject], message
except Exception:
    ContactMessage = None


def _ascii_header(text: str) -> str:
    """
    Para headers SMTP: quita guiones largos y tildes (ASCII-safe).
    """
    if not text:
        return ""
    text = text.replace("—", "-").replace("–", "-")
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()


def home(request):
    categories = Category.objects.all().order_by("id")
    products = Product.objects.select_related("category").all().order_by("-id")
    return render(request, "home.html", {"categories": categories, "products": products})


def contact_submit(request):
    if request.method != "POST":
        return redirect("home")

    # Honeypot
    if request.POST.get("website"):
        messages.error(request, "Solicitud inválida.")
        return redirect("home")

    name = (request.POST.get("nombre") or "").strip()
    phone = (request.POST.get("telefono") or "").strip()
    email = (request.POST.get("email") or "").strip()
    msg_text = (request.POST.get("mensaje") or "").strip()

    if not name or not msg_text:
        messages.error(request, "Por favor complete los campos obligatorios (nombre y mensaje).")
        return redirect("home")

    # SUBJECT seguro (ASCII-only)
    subject_raw = f"Contacto web - {name}"
    subject_safe = _ascii_header(subject_raw)[:255]

    # Guarda en BD (si existe el modelo)
    if ContactMessage is not None:
        try:
            data = dict(name=name, phone=phone, email=email, message=msg_text)
            if hasattr(ContactMessage, "subject"):
                data["subject"] = subject_raw
            ContactMessage.objects.create(**data)
        except Exception as e:
            # No bloquear por falla de guardado
            print("Advertencia al guardar mensaje:", e)

    # Cuerpo (UTF-8, no hay problema)
    body = (
        f"Nombre: {name}\n"
        f"Teléfono: {phone}\n"
        f"Correo: {email}\n"
        f"Mensaje:\n{msg_text}\n"
    )

    # FROM: solo la dirección (para evitar ASCII en headers)
    from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER

    # Destinatarios
    recipients = getattr(settings, "CONTACT_RECIPIENTS", []) or [from_email]
    recipients = [r for r in recipients if r]

    try:
        email_msg = EmailMessage(
            subject=subject_safe,
            body=body,
            from_email=from_email,
            to=recipients,
            headers={},  # sin headers extra para evitar issues de codificación
        )
        email_msg.encoding = "utf-8"
        email_msg.send(fail_silently=False)
        messages.success(request, "¡Su mensaje fue enviado correctamente!")
    except Exception as e:
        messages.warning(
            request,
            f"Su mensaje fue recibido, pero no se pudo enviar el correo en este momento. ({e})"
        )

    return redirect("home")
