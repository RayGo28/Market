# Market

Cryptocurrency market dashboard built with Django REST Framework, Celery, and Redis.

The application periodically fetches market data from the **CoinGecko API**, stores it in PostgreSQL, caches requests in Redis, and presents it via REST API and an interactive web interface.

## Tech Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Alpine.js
* **Backend:** Python 3.11, Django, Django REST Framework
* **Database:** PostgreSQL
* **Cache & Broker:** Redis
* **Background Tasks:** Celery, Celery Beat, Flower
* **Documentation:** Swagger / OpenAPI
* **Infrastructure:** Docker, Docker Compose

---

## Quick Start

### 1. Clone & Setup Environment

```bash
git clone [https://github.com/RayGo28/Market.git](https://github.com/RayGo28/Market.git)
cd Market
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata core_fixture.json
