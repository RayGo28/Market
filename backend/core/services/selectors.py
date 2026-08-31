from core.models import PriceHistory,Coin
from django.db.models import Count
from django.db.models import Avg, Max, Min
def get_coins_market_overview():
    coins = Coin.objects.filter(is_active=True).select_related("current_data").only(
        "id","name","symbol","current_data__price","current_data__market_cap",
        "current_data__total_volume","current_data__price_change_percentage_24h",
    )
    
    return coins

    
def get_coin_detail_overview(gecko_id):
    coin = Coin.objects.select_related("current_data").get(
                gecko_id=gecko_id,
                is_active=True
            )
    
    history = (
        PriceHistory.objects.filter(coin=coin)[:10]
    )

    coin.history_records = history
    
    stats = PriceHistory.objects.filter(coin=coin).aggregate(
        avg_price=Avg("price"),
        highest_price=Max("price"),
        lowest_price=Min("price"),
        history_records_count=Count("id"),
        first_recorded_at=Min("timestamp"),  
        last_updated_at=Max("timestamp")
    )

    coin.stats = stats

    return coin