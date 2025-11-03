from django.db import models

class Payment(models.Model):
    order_number = models.CharField(max_length=32)  # o ForeignKey a tu Order si ya lo tenés
    gateway = models.CharField(max_length=20)       # "placetopay" o "powertranz"
    request_id = models.CharField(max_length=64, blank=True)
    process_url = models.URLField(blank=True)
    status = models.CharField(max_length=32, default="created")  # created/APPROVED/REJECTED/...
    raw = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['order_number'])]

    def __str__(self):
        return f"{self.order_number} - {self.status}"
