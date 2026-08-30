import requests # type: ignore
from django.core.management.base import BaseCommand
from core.models import Coin

class Command(BaseCommand):
    help = "Автоматично завантажує Топ-100 монет з CoinGecko"

    def handle(self, *args, **options):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false"
        }

        self.stdout.write("Отримуємо дані з CoinGecko...")
        response = requests.get(url, params=params)

        if response.status_code != 200:
            self.stderr.write(f"Помилка запиту: {response.status_code}")
            return

        coins_data = response.json()
        created_count = 0
        updated_count = 0

        for item in coins_data:
            coin, created = Coin.objects.update_or_create(
                gecko_id=item["id"],
                defaults={
                    "name": item["name"],
                    "symbol": item["symbol"].lower(),
                    "image_url": item["image"],
                    "max_supply": item.get("max_supply"),
                    "is_active": True,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Успішно! Додано нових: {created_count}, оновлено: {updated_count}"
            )
        )