# Market

Cryptocurrency market dashboard built with Django, Django REST Framework, PostgreSQL, Redis and Celery.

The application fetches cryptocurrency market data from the CoinGecko API, stores it in PostgreSQL, caches data in Redis and periodically updates it using Celery.

## Tech Stack

* **Backend:** Python 3.11, Django, Django REST Framework
* **Frontend:** HTML, CSS, JavaScript, Alpine.js
* **Database:** PostgreSQL
* **Cache & Broker:** Redis
* **Background Tasks:** Celery, Celery Beat, Flower
* **Documentation:** Swagger / OpenAPI
* **Infrastructure:** Docker, Docker Compose
* **External API:** CoinGecko API

---

## Getting Started

1. **Clone the repository:**
   ```bash
   1.
   git clone [https://github.com/RayGo28/Market.git](https://github.com/RayGo28/Market.git)
   cd Market
   2.
   cp backend/.env.example backend/.env
   docker compose up --build -d
   3.
   docker compose exec web python manage.py migrate
   python manage.py fetch_coins
   4.
   docker compose exec web python manage.py shell -c "from watcher.tasks import update_market_data; update_market_data.delay()"
   docker compose exec web python manage.py shell -c "from watcher.tasks import update_global_data; update_global_data.delay()"
