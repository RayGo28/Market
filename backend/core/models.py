from django.db import models
from django.utils import timezone
class CryptoPrice(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10, db_index=True)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['symbol', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.name}({self.symbol}) - {self.price} at {self.timestamp}"