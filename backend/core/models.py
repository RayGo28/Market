from django.db import models

class CryptoPrice(models.Model):

    symbol = models.CharField(max_length=10, default="BTC")

    price = models.DecimalField(max_digits=20, decimal_places=2)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol}: {self.price} ({self.timestamp})"
    
