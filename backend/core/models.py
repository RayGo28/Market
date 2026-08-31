from django.db import models
from django.utils import timezone

class Coin(models.Model):
    gecko_id = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    max_supply = models.DecimalField(max_digits=38, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Coin"
        verbose_name_plural = "Coins"
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
class PriceHistory(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="history_data")
    
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True,blank=True)
    market_cap = models.DecimalField(max_digits=25, decimal_places=2, null=True,blank=True)
    total_volume = models.DecimalField(max_digits=25, decimal_places=2, null=True,blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    circulating_supply = models.DecimalField(max_digits=25, decimal_places=2, null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    atl = models.DecimalField(max_digits=20, decimal_places=8, null=True,blank=True)
    ath = models.DecimalField(max_digits=20, decimal_places=8, null=True,blank=True)
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['coin', '-timestamp']),
        ]
        verbose_name = "Price History"
        verbose_name_plural = "Price Histories"

    def __str__(self):
        price_str = f"${self.price}" if self.price is not None else "No Price"
        time_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else ""
        change_str = f"{self.price_change_percentage_24h}%" if self.price_change_percentage_24h is not None else "0.00%"
        return f"{self.coin.symbol} | {price_str} | {time_str} | {change_str}"
    
class CoinCurrentData(models.Model):
    coin = models.OneToOneField(Coin,on_delete=models.CASCADE,related_name='current_data')
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True,blank=True)
    market_cap = models.DecimalField(max_digits=25, decimal_places=2, null=True,blank=True)
    total_volume = models.DecimalField(max_digits=25, decimal_places=2, null=True,blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    circulating_supply = models.DecimalField(max_digits=25, decimal_places=2, null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    atl = models.DecimalField(max_digits=20, decimal_places=8, null=True,blank=True)
    ath = models.DecimalField(max_digits=20, decimal_places=8, null=True,blank=True)
    class Meta:
        verbose_name = "Coin Current Data"
        verbose_name_plural = "Coins Current Data"
    