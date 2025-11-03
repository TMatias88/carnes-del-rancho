from django.urls import path
from . import views

urlpatterns = [
    path("contacto/enviar/", views.contact_submit, name="contact_submit"),
    path("", views.home, name="home"),
]
