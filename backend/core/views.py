from django.shortcuts import render,get_object_or_404
from .models import Coin, PriceHistory
from django.db.models import Avg, Max, Min, Count

def index(request):
    qs = Coin.objects.all()

    data = {
        "coins": qs
    }

    return render(request, 'main/index.html', data)

def crypto_detail(request, symbol):

    coin = get_object_or_404(Coin.objects.prefetch_related('all'), symbol__iexact=symbol)

    return render(request, "main/crypto_detail.html", {"coin": coin})
    
    
    




