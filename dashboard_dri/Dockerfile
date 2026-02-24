FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système (si besoin: pandas, scipy, etc. parfois nécessitent build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Dash tourne sur 8050 par défaut
EXPOSE 8050

# Gunicorn sert l'app Flask sous-jacente
# app:server = fichier app.py, variable server
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server", "--workers=2", "--threads=4", "--timeout=120"]

