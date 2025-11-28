# Codigo para mandar angulos al esp
import esp32_sender
from trayectoria import csv_to_theta

l1 = 100
l2 = 150
l5 = 106.249
Esp = esp32_sender.ESP32Sender()

points = csv_to_theta(
    "./paths/cuadrado.csv",
    l1,
    l2,
    l5,
)


for t1, t2 in points:
    t1 = round(t1, 2)
    t2 = round(t2, 2)
    Esp.send_angles(t1, t2)
    print(f"angulos: {t1}, {t2}")


Esp.close()
