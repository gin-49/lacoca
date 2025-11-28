# Code que se va subir al ESP32

from stepper import Stepper
from receiver import read_angles, send_ok
import time

# Estableciendo los puerto
s1 = Stepper(16, 17, steps_per_rev=3200, speed_sps=2000, timer_id=0)
s2 = Stepper(18, 19, steps_per_rev=3200, speed_sps=2000, timer_id=1)

while True:
    result = read_angles()
    if result is None:
        print("Error")
        continue

    t1, t2 = result
    t1 = t1 - 90
    t2 = -t2 + 90

    s1.target_deg(t1)
    s2.target_deg(t2)
    send_ok(t1, t2)
    time.sleep(1)
