# Code que se va subir al ESP32
from stepper import Stepper
from servo import Servo
import time

# Estableciendo los puertos
s1 = Stepper(16, 17, steps_per_rev=3200, speed_sps=1500, timer_id=0)
s2 = Stepper(18, 19, steps_per_rev=3200, speed_sps=1500, timer_id=1)

servo = Servo(26)
angles = []
all_angles = []

servo.move(0)

# Lee el .csv
filepath = "/generated_paths/triangulo_angles.csv"
with open(filepath, "r") as file:
    for line in file:
        angles = [float(x) for x in line.strip().split(",")]
        all_angles.append(angles)

# get_pos_deg()
# speed(sps)
# target_deg(deg)

for t1, t2 in all_angles:
    s1.target_deg(t1)
    s2.target_deg(t2)
    time.sleep(1)
    servo.move(190)
    time.sleep(2)
