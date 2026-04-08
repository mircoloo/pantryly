FROM python:3.11-slim

WORKDIR /app

# Copiamo prima solo i requirements per sfruttare la cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il codice sorgente
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
