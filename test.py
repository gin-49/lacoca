from stepper import Stepper
from servo import Servo
import time

s1 = Stepper(16, 17, steps_per_rev=3200, speed_sps=500, timer_id=0)
s2 = Stepper(18, 19, steps_per_rev=3200, speed_sps=500, timer_id=1)
servo = Servo(26)

while True:
    s1.target_deg(61)
    s2.target_deg(28)
    time.sleep(3)
    s1.target_deg(0)
    s2.target_deg(0)
    time.sleep(3)
