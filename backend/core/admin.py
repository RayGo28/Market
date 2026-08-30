from django.contrib import admin
from django.utils import timezone
from .models import Coin, CoinCurrentData, PriceHistory

@admin.display(description="Timestamp", ordering="timestamp")
def timestamp_24h(obj):
    if obj.timestamp is None:
        return "No Timestamp"
    local_time = timezone.localtime(obj.timestamp)
    return local_time.strftime("%d.%m.%Y %H:%M")


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('gecko_id', 'name', 'symbol', 'max_supply', 'is_active')
    list_filter = ('name', 'symbol')
    
@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("coin", "price", "market_cap", "total_volume", "price_change_percentage_24h", timestamp_24h)
    list_filter = ("coin", "timestamp")


@admin.register(CoinCurrentData)
class CoinCurrentDataAdmin(admin.ModelAdmin):
    list_display = ("coin", "price", "market_cap", "total_volume", "price_change_percentage_24h", timestamp_24h)
    list_filter = ("coin", "timestamp")
