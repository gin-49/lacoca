from stepper import Stepper
import time

s1 = Stepper(18, 19, steps_per_rev=3200, speed_sps=1500, timer_id=0)

while True:
    s1.target_deg(-180)
    time.sleep(4.0)
    s1.target_deg(0)
    time.sleep(4.0)
