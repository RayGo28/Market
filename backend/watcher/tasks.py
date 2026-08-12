from celery import shared_task  # type: ignore
import requests # type: ignore
from core.models import Coin, PriceHistory
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

coins = list(Coin.objects.filter(is_active=True).values_list("coin_id", flat=True))


    