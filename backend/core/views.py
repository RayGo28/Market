from django.shortcuts import render
from .models import CryptoPrice
from django.db.models import Avg, Max, Min, Count

def index(request):
    qs = CryptoPrice.objects.order_by("symbol", "-timestamp").distinct("symbol")
    
    data = {
        "coins": qs
    }

    return render(request, 'main/index.html', data)
    




