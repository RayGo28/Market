from django.shortcuts import render
from .models import CryptoPrice
from django.db.models import Avg, Max, Min, Count

def index(request):
    qs = CryptoPrice.objects.values("symbol").distinct()
    data = {
        "cryptos" : qs
    }
    return render(request, "main/index.html", data)

def crypto_detail(request, symbol):
    crypto = CryptoPrice.objects.filter(symbol=symbol).order_by("-timestamp").first()
    
    if not crypto:
        return render(request, "main/crypto_detail.html", {"crypto": None})
    
    data = {
        "crypto" : crypto
    }
    
    return render(request, "main/crypto_detail.html", data)

def stats_btc(request):
    last_30 = CryptoPrice.objects.filter(symbol = "BTC").order_by("-timestamp").values_list('id', flat=True)[:30]
    
    stats = CryptoPrice.objects.filter(id__in = last_30).aggregate(
        avg_price=Avg('price'),
        total_count=Count('id') 
    )
    
    btc = CryptoPrice.objects.order_by("-timestamp").filter(symbol="BTC").first()
    trend = "up" if btc.price > stats['avg_price'] else "down"
    
    if not btc:
        return render(request, "main/btc.html", {"bitcoin": None})
    
    
    data = {
        "bitcoin" : {
            "price" : btc.price,
            "avg" : stats['avg_price'],
            "total" : stats['total_count'],
            'trend' : trend
        }
    }
    
    return render(request, "main/btc.html", data)





