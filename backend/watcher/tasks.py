import logging
from core.serializers import CoinSerializer
from celery import shared_task  # type: ignore
import requests # type: ignore
from core.models import Coin, PriceHistory,CoinCurrentData
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

headers = {
    "x-cg-demo-api-key": settings.COINGECKO_API_KEY
}


TASK_SETTINGS = {
    'bind': True,
    'autoretry_for': (requests.RequestException,),
    'retry_backoff': True,
    'retry_kwargs': {'max_retries': 3}
}



@shared_task(**TASK_SETTINGS)
def fetch_cryptocurrency(self):
    active_coins = Coin.objects.filter(is_active=True).in_bulk(field_name="gecko_id")
    
    if not active_coins:
        logger.info("No active coins found.")
        return "No active coins found."
    
    coins_ids_param = ",".join(active_coins.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coins_ids_param}"
    
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    market_data = response.json()
    
    records_data = []
    recieved_ids = []
    
    update_fields = []

    for field in CoinCurrentData._meta.concrete_fields:
        if field.name != 'id' and field.name != 'coin':
            update_fields.append(field.name)
    
    if isinstance(market_data, list):
        for coin_market_info in market_data:
            coin_instance = active_coins.get(coin_market_info["id"])
            if coin_instance:
                recieved_ids.append(coin_market_info["id"])
                data_kwargs = {
                                            'coin': coin_instance,
                                            'price': coin_market_info.get("current_price"),
                                            'market_cap': coin_market_info.get("market_cap"),
                                            'total_volume': coin_market_info.get("total_volume"),
                                            'price_change_percentage_24h': coin_market_info.get("price_change_percentage_24h")
                }
                records_data.append(data_kwargs)
                
        for coin_id in active_coins:
            if coin_id not in recieved_ids:
                logger.warning(f"Coin {coin_id} not returned from API.")
    if records_data:
        PriceHistory.objects.bulk_create([PriceHistory(**item) for item in records_data])
        CoinCurrentData.objects.bulk_create(
                            [CoinCurrentData(**item) for item in records_data],
                            update_conflicts=True,
                            unique_fields=['coin'],
                            update_fields=update_fields
                        )
        logger.info(f"Data is updated for {len(records_data)} coins.")

        updated_coins = Coin.objects.filter(is_active=True).select_related('current_data')
        serializer = CoinSerializer(updated_coins, many=True)
        
        cache.set('coin_list_cache', serializer.data, timeout=65)
    
    
    return f"Fetched and stored price history for {len(records_data)} coins out of {len(active_coins)}."

    