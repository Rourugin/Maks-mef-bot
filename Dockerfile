FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir \ 
    aiogram \ 
    aiosqlite \ 
    asyncio \ 
    dotenv \ 
    pymorphy3

CMD ["python", "main.py"]