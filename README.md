# Market

Short description

## Features
- Cryptocurrency market dashboard
- Coin details
- Price history
- Search / filtering / sorting
- Background market updates
- Redis caching
- REST API
- Swagger/OpenAPI

## Architecture

Frontend
   ↓
Django / DRF
   ↓
Redis cache
   ↓
PostgreSQL

Celery Beat
   ↓
Celery Worker
   ↓
CoinGecko API
   ↓
PostgreSQL + Redis

## Tech Stack

...

## Project Structure

...

## Requirements

...

## Environment Variables

...

## Getting Started

git clone ...
cd Market
cp backend/.env.example backend/.env
docker compose up --build

## Database Initialization

docker compose exec web python manage.py migrate
docker compose exec web python manage.py fetch_coins

## API

GET /api/coins/
GET /api/coins/{gecko_id}/
GET /api/global/

Swagger:
http://localhost:8000/api/docs/

OpenAPI:
http://localhost:8000/api/schema/

## Background Tasks

Market updates every 120 sec
Global data every 600 sec

## Development

...

## License
