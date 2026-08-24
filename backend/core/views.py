from django.shortcuts import render,get_object_or_404
from .models import Coin, PriceHistory
from django.db.models import Avg, Max, Min, Count, Prefetch

def index(request):

    coins = Coin.objects.all() 

    return render(request, 'main/index.html', {"coins": coins})


    




