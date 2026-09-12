FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fresh DB on every container start (no state carried between runs)
RUN rm -f tinycorp.db

EXPOSE 5000

CMD ["python3", "app.py"]
