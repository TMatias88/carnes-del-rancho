from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Mantén SOLO un include del admin (conserva tu URL “segura”)
    path("dashboard-securo-789/", admin.site.urls),

    # Redirige /admin/ hacia la ruta segura (no añade otro namespace)
    path("admin/", RedirectView.as_view(url="/dashboard-securo-789/", permanent=False)),

    path("", include("pages.urls")),
    path("catalogo/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("payments/", include(("payments.urls", "payments"), namespace="payments")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
