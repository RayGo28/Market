from django.shortcuts import render
from .models import Coin, PriceHistory
from django.db.models import Avg, Max, Min, Count

def index(request):
    qs = Coin.objects.all()

    data = {
        "coins": qs
    }

    return render(request, 'main/index.html', data)
    




