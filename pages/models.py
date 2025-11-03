from django.db import models

class ContactMessage(models.Model):
    name = models.CharField("Nombre", max_length=120)
    phone = models.CharField("Teléfono", max_length=30, blank=True)
    email = models.EmailField("Correo", blank=True)
    subject = models.CharField("Asunto", max_length=200)
    message = models.TextField("Mensaje")
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    is_read = models.BooleanField("Leído", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.name} - {self.subject}"
