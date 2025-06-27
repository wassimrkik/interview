FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", \
#      "--ssl-keyfile=/certs/code-server.tailb8fd1f.ts.net.key", \
#      "--ssl-certfile=/certs/code-server.tailb8fd1f.ts.net.crt"]
