from django.urls import include, path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("thanks/", views.order_thanks, name="order_thanks"),
    path("pagos/", include("payments.urls")),
]
