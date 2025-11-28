from stepper import Stepper
import time

s1 = Stepper(18, 19, steps_per_rev=3200, speed_sps=2000, timer_id=0)
s2 = Stepper(16, 17, steps_per_rev=3200, speed_sps=2000, timer_id=1)

while True:
    s1.target_deg(-180)
    s2.target_deg(180)
    time.sleep(2.0)
    s1.target_deg(0)
    s2.target_deg(0)
    time.sleep(2.0)
