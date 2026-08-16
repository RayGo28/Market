from django.contrib import admin
from django.utils import timezone
from .models import Coin, PriceHistory


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("coin_id", "name", "symbol", "max_supply", "is_active")
    list_filter = ('name', 'symbol')
    
@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("coin", "price","market_cap","total_volume","price_change_percentage_24h", "timestamp")
    list_filter = ("coin", "timestamp")
