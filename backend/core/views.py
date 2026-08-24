from django.shortcuts import render,get_object_or_404
from .models import Coin, PriceHistory
from django.db.models import Avg, Max, Min, Count, Prefetch

def index(request):
    latest_history = PriceHistory.objects.order_by('coin', '-timestamp').distinct('coin')

    coins = Coin.objects.filter(is_active=True).prefetch_related(
        Prefetch('market_data', queryset=latest_history)
    )

    return render(request, 'main/index.html', {"coins": coins})


    




