import logging
from celery import shared_task  # type: ignore
import requests # type: ignore
from core.models import Coin, PriceHistory
from django.conf import settings

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
    active_coins = Coin.objects.filter(is_active=True).in_bulk(field_name="coin_id")
    
    if not active_coins:
        logger.info("No active coins found.")
        return "No active coins found."
    
    coins_ids_param = ",".join(active_coins.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coins_ids_param}"
    
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    market_data = response.json()
    
    history_records =[]
    recieved_ids = []
    
    if isinstance(market_data, list):
        for coin_market_info in market_data:
            coin_instance = active_coins.get(coin_market_info["id"])
            if coin_instance:
                recieved_ids.append(coin_market_info["id"])
                history_records.append(PriceHistory(coin = coin_instance,
                                            price = coin_market_info.get("current_price"),
                                            market_cap = coin_market_info.get("market_cap"),
                                            total_volume = coin_market_info.get("total_volume"),
                                            price_change_percentage_24h = coin_market_info.get("price_change_percentage_24h")
                                            ))
        for coin_id in active_coins:
            if coin_id not in recieved_ids:
                logger.warning(f"Coin {coin_id} not returned from API.")
    if history_records:
        PriceHistory.objects.bulk_create(history_records)
        
    return f"Fetched and stored price history for {len(history_records)} coins out of {len(active_coins)}."

    