from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog_view, name="catalogo"),  # /catalogo/
    path("<slug:category_slug>/", views.catalog_view, name="catalogo_por_categoria"),  # /catalogo/<slug>/
]
