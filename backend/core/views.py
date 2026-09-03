from django.shortcuts import render
from core.services.selectors import get_coins_market_overview, get_coin_detail_overview
from .serializers import CoinListSerializer, CoinDetailSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


def index(request):
    
    return render(request, 'main/index.html')

def coin_detail_page(request, pk):
    return render(request, 'main/coin_detail.html', {'str': pk})

class Coins(ReadOnlyModelViewSet):
    queryset = get_coins_market_overview()
    serializer_class = CoinListSerializer
    permission_classes = [AllowAny]
    lookup_field = 'gecko_id'
    
    def get_queryset(self):
        return get_coins_market_overview()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return CoinDetailSerializer

        elif self.action == "list":
            return CoinListSerializer
     
    def list(self, request, *args, **kwargs):
        cache_key = 'coin_list_cache'
        data = cache.get(cache_key)
        
        if data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            
            cache.set(cache_key, data, 125)
        
        search_query = request.query_params.get('search', '').strip().lower()
        if search_query:
            filtered_data = []
            for coin in data:
                name = str(coin.get('name', '')).lower()
                symbol = str(coin.get('symbol', '')).lower()
                

                if search_query in name or search_query in symbol:
                    filtered_data.append(coin)
                    
            data = filtered_data
            
        return Response(data)
    
    def retrieve(self, request, *args, **kwargs):
        gecko_id = kwargs["gecko_id"]
        cache_key = f"coin_detail_{gecko_id}"
        
        data = cache.get(cache_key)
        
        if data is None:
            coin = get_coin_detail_overview(gecko_id)
            serializer = self.get_serializer(coin)
            data = serializer.data
            cache.set(cache_key, data, timeout = 125)
    
        return Response(data)
    
        
        

        
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_global_data(request):
    data = cache.get("global_data")
    
    if data is None:
        data = {
                    "total_market_cap" : None,
                    "total_volume" : None,
                    "market_cap_percentage_btc" : None,
                    "active_coins_count" : None  
                }
        
    return Response(data)