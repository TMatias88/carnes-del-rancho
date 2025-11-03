from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("iniciar/<str:order_number>/", views.iniciar_pago, name="start"),
    path("retorno/", views.retorno_pago, name="return"),
    path("webhook/", views.webhook_pago, name="webhook"),
]
