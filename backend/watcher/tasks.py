from celery import shared_task 
import requests
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
        new_entry = CryptoPrice.objects.create(symbol="BTC", price=current_price)
        
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
        new_entry = CryptoPrice.objects.create(symbol="ETHEREUM", price=current_price)
        
        return f"Ціна {current_price} збережена в базу о {new_entry.timestamp}"
    return "Помилка: не вдалося отримати дані про ефір."

