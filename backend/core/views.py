from django.shortcuts import render
from .models import Coin,CoinCurrentData
from .serializers import CoinSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache
from rest_framework.response import Response

def index(request):
    
    return render(request, 'main/index.html')

class CoinList(ReadOnlyModelViewSet):
    queryset = Coin.objects.filter(is_active=True).select_related('current_data')
    serializer_class = CoinSerializer
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