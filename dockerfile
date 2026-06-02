FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gpiozero pigpio smbus2 RPi.bme280

COPY . .

CMD ["python3", "-u", "main.py"]
