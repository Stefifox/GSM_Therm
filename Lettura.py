import Adafruit_DHT

DHT11 = Adafruit_DHT.DHT11
DHT11_PIN = 12


def temp():
    umidita, temperatura = Adafruit_DHT.read_retry(DHT11, DHT11_PIN, retries=10, delay_seconds=1)
    return temperatura


def umid():
    umidita, temperatura = Adafruit_DHT.read_retry(DHT11, DHT11_PIN, retries=10, delay_seconds=1)
    return umidita