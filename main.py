# Code que se va subir al ESP32

from stepper import Stepper
import time

s1 = Stepper(18, 19, steps_per_rev=3200, speed_sps=1500, timer_id=0)
s2 = Stepper(16, 17, steps_per_rev=3200, speed_sps=1500, timer_id=1)

while True:
    theta1 = float(input("theta1: "))
    s1.target_deg(theta1)
    print("Movement started")
