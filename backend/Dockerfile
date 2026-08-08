FROM python:3.11-slim

# щоб не було лагів з логами
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# системні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# встановлюємо залежності
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# копіюємо код
COPY . .

# порт
EXPOSE 8000
