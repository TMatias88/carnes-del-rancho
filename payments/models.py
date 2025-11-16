# payments/models.py
from django.db import models


class Payment(models.Model):
    GATEWAY_CHOICES = [
        ("placetopay", "PlaceToPay"),
        ("otro", "Otro"),
    ]

    order_number = models.CharField(max_length=64, db_index=True)
    gateway = models.CharField(max_length=32, choices=GATEWAY_CHOICES, default="placetopay")
    request_id = models.CharField(max_length=64, blank=True, null=True)
    process_url = models.URLField(blank=True, null=True)

    status = models.CharField(max_length=64, default="created")
    raw = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} [{self.gateway}] {self.status}"
