from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from catalog.utils.images import resolve_image


class Category(models.Model):
    name = models.CharField("Nombre", max_length=80, unique=True)
    slug = models.SlugField("Slug", unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
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

    # 🔥 Campo real para archivos locales
    image_file = models.ImageField(
        "Imagen local (solo desarrollo)",
        upload_to="products/",
        blank=True,
        null=True,
    )

    # 🔥 Campo para RAW
    image_url = models.URLField(
        "URL de imagen RAW (GitHub/DO)",
        max_length=500,
        blank=True,
        null=True,
    )

    price_crc = models.DecimalField(
        "Precio (CRC)", max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    stock = models.PositiveIntegerField("Stock", default=0)
    is_active = models.BooleanField("Activo", default=True)

    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # PROPIEDAD FINAL: el template usa solo esto
    @property
    def final_image(self):
        return resolve_image(self)

    @property
    def price_crc_display(self):
        return f"₡{self.price_crc:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
