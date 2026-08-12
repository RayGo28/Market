from celery import shared_task  # type: ignore
import requests # type: ignore
from core.models import CryptoPrice
from django.conf import settings

headers = {
    "api-key": settings.COINGECKO_API_KEY
}

CRYPTO_MAP = {
    'bitcoin': {'name': 'Bitcoin', 'symbol': 'BTC'},
    'ethereum': {'name': 'Ethereum', 'symbol': 'ETH'},
    'tether': {'name': 'Tether', 'symbol': 'USDT'},
    'usd-coin': {'name': 'USD Coin', 'symbol': 'USDC'},
}

TASK_SETTINGS = {
    'bind': True,
    'autoretry_for': (requests.RequestException,),
    'retry_backoff': True,
    'retry_kwargs': {'max_retries': 3}
}

@shared_task(**TASK_SETTINGS)
def fetch_crypto_prices(self):
    ids = ",".join(CRYPTO_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&precision=2"
    
    headers = {
        "x-cg-demo-api-key": settings.COINGECKO_API_KEY
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    failed_coins = []
    objects_to_create = []  
    
    for coin_id, coin_info in CRYPTO_MAP.items():
        coin_data = data.get(coin_id)
        if coin_data and 'usd' in coin_data:
            objects_to_create.append(
                CryptoPrice(
                    name=coin_info['name'],
                    symbol=coin_info['symbol'],
                    price=coin_data['usd']
                )
            )
        else:
            failed_coins.append(coin_id)

    if objects_to_create:
        CryptoPrice.objects.bulk_create(objects_to_create)

    return (
        f"Successfully updated coins: {len(objects_to_create)}\n"
        f"Failed coins: {failed_coins}"
    )