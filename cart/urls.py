from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_view, name="cart_view"),
    path("agregar/<int:product_id>/", views.add_to_cart, name="cart_add"),
    path("eliminar/<int:product_id>/", views.remove_item, name="cart_remove"),
    path("vaciar/", views.clear_cart, name="cart_clear"),
    path("panel/", views.cart_panel, name="cart_panel"),

]
