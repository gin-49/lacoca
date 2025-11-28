# Code que se va subir al ESP32

from stepper import Stepper
from receiver import read_angles, send_ok
import time

s1 = Stepper(18, 19, steps_per_rev=3200, speed_sps=3200, timer_id=0)
s2 = Stepper(16, 17, steps_per_rev=3200, speed_sps=3200, timer_id=1)

while True:
    result = read_angles()
    if result is None:
        print("ERR unpack")
        continue

    t1, t2 = result

    # Send confirmation
    send_ok(t1, t2)

    # Move motors
    s1.target_deg(t1)
    s2.target_deg(t2)
    time.sleep(3)
