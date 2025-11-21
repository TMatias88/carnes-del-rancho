from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Nombre", max_length=80, unique=True)
    slug = models.SlugField("Slug", unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalogo_por_categoria", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Categoría",
    )
    name = models.CharField("Nombre", max_length=120)
    slug = models.SlugField("Slug", unique=True, blank=True)
    description = models.TextField("Descripción", blank=True)

    # ⬇️⬇️ CAMBIO IMPORTANTE: AHORA ES UNA URL, NO UN ARCHIVO ⬇️⬇️
    image_url = models.URLField(
        "URL de imagen RAW (GitHub u otra)",
        max_length=500,
        blank=True,
        null=True
    )

    price_crc = models.DecimalField(
        "Precio (CRC)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Precio en colones costarricenses (₡).",
    )
    stock = models.PositiveIntegerField("Stock", default=0)
    is_active = models.BooleanField("Activo", default=True)
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalogo")

    @property
    def price_crc_display(self) -> str:
        return f"₡{self.price_crc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
