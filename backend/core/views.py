from django.shortcuts import render
from .models import Coin,CoinCurrentData
from .serializers import CoinListSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

def index(request):
    
    return render(request, 'main/index.html')

class Coins(ReadOnlyModelViewSet):
    queryset = Coin.objects.filter(is_active=True).select_related('current_data')
    serializer_class = CoinListSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwarqs):
        cache_key = 'coin_list_cache'
        data = cache.get(cache_key)
        
        if data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            
            cache.set(cache_key, data, 65)
        
        return Response(data)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_global_data(request):
    data = cache.get("global_data")
    
    if data is None:
        data = {
                    "total_market_cap" : None,
                    "total_volume" : None,
                    "market_cap_percentage" : None,
                    "active_coins_count" : None  
                }
        
    return Response(data)