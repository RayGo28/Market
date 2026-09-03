from decimal import Decimal, InvalidOperation

from django.db import transaction

from core.services.coingecko import fetch_market_data, fetch_global_data
from core.models import Coin,CoinCurrentData,PriceHistory
from django.core.cache import cache
import logging
from core.serializers import CoinListSerializer
from core.services.selectors import get_coins_market_overview

logger = logging.getLogger(__name__)

def prepare_records_data(raw_data, active_coins):
    records_data = []
    received_ids = [] 
    
    if isinstance(raw_data, list):
        for coin_market_info in raw_data:         
            coin_instance = active_coins.get(coin_market_info["id"])
            if coin_instance:
                received_ids.append(coin_market_info["id"])
                
                ath_raw = coin_market_info.get("ath")
                atl_raw = coin_market_info.get("atl")
                
                try:
                    ath_val = Decimal(str(ath_raw)) if ath_raw is not None else None
                except (InvalidOperation, TypeError):
                    ath_val = None
                    
                try:
                    atl_val = Decimal(str(atl_raw)) if atl_raw is not None else None
                except (InvalidOperation, TypeError):
                    atl_val = None
                    
                data_kwargs = {
                                'coin': coin_instance,
                                'price': coin_market_info.get("current_price"),
                                'market_cap': coin_market_info.get("market_cap"),
                                'total_volume': coin_market_info.get("total_volume"),
                                'price_change_percentage_24h': coin_market_info.get("price_change_percentage_24h"),
                                'circulating_supply': coin_market_info.get("circulating_supply"),
                                'atl' : atl_val,
                                'ath' : ath_val,
                }
                        
                records_data.append(data_kwargs)    
        for coin_id in active_coins:
            if coin_id not in received_ids:
                logger.warning(f"Coin {coin_id} not returned from API.")
    
    return records_data

def save_market_data(records_data):
    update_fields = [
        'price',
        'market_cap',
        'total_volume',
        'price_change_percentage_24h',
        'circulating_supply',
        'ath',
        'atl',
        'timestamp'
    ]
    
    if records_data:
        with transaction.atomic():
            PriceHistory.objects.bulk_create([PriceHistory(**item) for item in records_data])
            CoinCurrentData.objects.bulk_create(
                                [CoinCurrentData(**item) for item in records_data],
                                update_conflicts=True,
                                unique_fields=['coin'],
                                update_fields=update_fields
                            )
                
        logger.info(f"Data is updated for {len(records_data)} coins.")
        
def update_cache_coin_list():
    updated_coins = get_coins_market_overview()
    serializer = CoinListSerializer(updated_coins, many=True)
    cache.set('coin_list_cache', serializer.data, timeout=125)
            
def sync_market_data():

    active_coins = Coin.objects.filter(is_active=True).in_bulk(field_name="gecko_id")
    if not active_coins:
        logger.info("No active coins found.")
        return "No active coins found."

    coin_ids_param = ",".join(active_coins.keys())
    
    raw_data = fetch_market_data(coin_ids_param)
    records_data = prepare_records_data(raw_data, active_coins)
    save_market_data(records_data)
    update_cache_coin_list()
    
    return f"Fetched and stored price history for {len(records_data)} coins out of {len(active_coins)}."
 
    
def sync_global_data():
    raw_data = fetch_global_data()
    
    active_coins_count = Coin.objects.filter(is_active=True).count()

    global_data = {}
        
    if isinstance(raw_data, dict):
        global_data = {
            "total_market_cap" : raw_data["total_market_cap"]["usd"],
            "total_volume" : raw_data["total_volume"]["usd"],
            "market_cap_percentage_btc" : raw_data["market_cap_percentage"]["btc"],
            "active_coins_count" : active_coins_count,   
            "market_cap_change_percentage_24h_usd" : raw_data["market_cap_change_percentage_24h_usd"],
            "volume_change_percentage_24h_usd" : raw_data["volume_change_percentage_24h_usd"]
        }
        
    if global_data:
        cache.set("global_data",global_data, timeout=620)

    return f"Fetched and stored global data: {global_data}"