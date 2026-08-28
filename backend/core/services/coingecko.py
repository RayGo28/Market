from wsgiref import headers
import requests # type: ignore
from config import settings
import logging

logger = logging.getLogger(__name__)

headers = {
    "x-cg-demo-api-key": settings.COINGECKO_API_KEY
}

def fetch_market_data(coins_ids_param):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coins_ids_param}"
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    raw_data = response.json()
    
    return raw_data


def fetch_global_data():
    url = "https://api.coingecko.com/api/v3/global"
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    raw_data = response.json().get("data", {})
    
    return raw_data