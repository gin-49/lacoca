from machine import Pin
import time

# Definir los pines
pins = [16, 17, 18, 19]
leds = [Pin(p, Pin.OUT) for p in pins]

while True:
    # Encender todos los LEDs
    for led in leds:
        led.value(1)
    time.sleep(0.5)  # espera 500 ms

    # Apagar todos los LEDs
    for led in leds:
        led.value(0)
    time.sleep(0.5)
