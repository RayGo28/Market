from celery import shared_task  # type: ignore
import requests # type: ignore
from core.models import CryptoPrice


TASK_SETTINGS = {
    'bind': True,
    'autoretry_for': (Exception,),
    'retry_backoff': True,
    'retry_kwargs': {'max_retries': 3}
}

@shared_task(**TASK_SETTINGS)
def fetch_btc_price(self):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&precision=2"
    response = requests.get(url)
    data = response.json()
    
    bitcoin = data.get('bitcoin')
    if bitcoin:
        current_price = bitcoin['usd']
        new_entry = CryptoPrice.objects.create(name="Bitcoin",symbol="BTC", price=current_price)
        
        return f"Ціна {current_price} збережена в базу о {new_entry.timestamp}"
    return "Помилка: Не вдалося отримати дані про ціну біткоїна."

@shared_task(**TASK_SETTINGS)
def fetch_eth_price(self):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&precision=2"
    response = requests.get(url)
    data = response.json()
    
    etherium = data.get("ethereum")
    if etherium:
        current_price = etherium['usd']
        new_entry = CryptoPrice.objects.create(name="Ethereum",symbol="ETH", price=current_price)
        
        return f"Ціна {current_price} збережена в базу о {new_entry.timestamp}"
    return "Помилка: не вдалося отримати дані про ефір."


@shared_task(**TASK_SETTINGS)
def fetch_tether_price(self):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd&precision=2"
    response = requests.get(url)
    data = response.json()
    
    tether = data.get("tether")
    if tether:
        current_price = tether["price"]
        new_entry = CryptoPrice.object.create(name="Tether",symbol="USDT", price=current_price)
        
        return f"Ціна {current_price} збережена в базу о {new_entry.timestamp}"
    return "Помилка: не вдалося отримати дані про тезер."