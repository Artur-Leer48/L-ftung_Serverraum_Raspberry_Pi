FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir gpiozero pigpio smbus2 RPi.bme280

COPY main.py .

CMD ["python3", "-u", "main.py"]
