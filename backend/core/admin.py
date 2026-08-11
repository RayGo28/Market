from django.contrib import admin
from django.utils import timezone
from .models import CryptoPrice


@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'price', 'timestamp_24')
    list_filter = ('name', 'symbol', 'timestamp')

    def timestamp_24(self, obj):
        ts = timezone.localtime(obj.timestamp)
        return ts.strftime('%d %b %Y, %H:%M')

    timestamp_24.short_description = 'Timestamp'
    timestamp_24.admin_order_field = 'timestamp'
    