from django.contrib import admin
from .models import CryptoPrice

@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'price', 'timestamp') 
    list_filter = ('symbol', 'timestamp') 
    
