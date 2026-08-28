import logging
from celery import shared_task  # type: ignore
import requests # type: ignore
from core.services.coin_sync import sync_market_data, sync_global_data

logger = logging.getLogger(__name__)

TASK_SETTINGS = {
    'bind': True,
    'autoretry_for': (requests.RequestException,),
    'retry_backoff': True,
    'retry_kwargs': {'max_retries': 3}
}

@shared_task(**TASK_SETTINGS)
def update_market_data(self):
    sync_market_data()
    
@shared_task(**TASK_SETTINGS)
def update_global_data(self):
    sync_global_data()
    