from core.models import PriceHistory,Coin,CoinCurrentData
from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, FloatField
from django.utils import timezone
from core.serializers import CoinListSerializer
from django.core.cache import cache

def get_coins_market_overview():
    time_24h_ago = timezone.now() - timezone.timedelta(hours=24)
    
    price_24h_ago = PriceHistory.objects.filter(
                    coin = OuterRef("pk"),
                    timestamp__lte = time_24h_ago,
                ).values("price")[:1]
    
    coins = Coin.objects.filter(is_active=True).select_related("current_data").annotate(
        price_24h_ago = Subquery(price_24h_ago),
        change_percent = ExpressionWrapper((F("current_data__price") - F("price_24h_ago")) / F("price_24h_ago") * 100,
                                        output_field = FloatField())
    
    )
    
    return coins
    
    
    
    
    
    