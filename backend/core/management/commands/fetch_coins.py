import logging
import requests  # type: ignore
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Coin
from watcher.tasks import update_global_data, update_market_data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Завантажує Топ-100 монет з CoinGecko та запускає фонові таски для оновлення ринку"

    def handle(self, *args, **options):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false",
        }

        self.stdout.write("Отримуємо Топ-100 монет з CoinGecko...")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            coins_data = response.json()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Помилка при запиті до CoinGecko: {e}"))
            return

        created_count = 0
        updated_count = 0


        with transaction.atomic():
            for item in coins_data:
                _, created = Coin.objects.update_or_create(
                    gecko_id=item["id"],
                    defaults={
                        "name": item["name"],
                        "symbol": item["symbol"].lower(),
                        "image_url": item["image"],
                        "max_supply": item.get("max_supply"),
                        "is_active": True,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"База заповнена! Нових монет: {created_count}, оновлено: {updated_count}"
            )
        )


        self.stdout.write("Запускаємо фонові таски оновлення ринку та глобальних даних...")
        try:
            update_market_data.delay()
            update_global_data.delay()
            self.stdout.write(self.style.SUCCESS("Таски Celery успішно відправлені в чергу!"))
        except Exception as e:
            self.stderr.write(
                self.style.WARNING(
                    f"Не вдалося запустити Celery таски (перевірте Redis/Broker): {e}"
                )
            )