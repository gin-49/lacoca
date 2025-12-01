# Code que se va subir al ESP32 - Random Iteration
from stepper import Stepper
from servo import Servo
import time

# Try to import random, fall back to urandom if not available
try:
    import random
except ImportError:
    import urandom as random

# Estableciendo los puertos
s1 = Stepper(16, 17, steps_per_rev=3200, speed_sps=500, timer_id=0)
s2 = Stepper(18, 19, steps_per_rev=3200, speed_sps=500, timer_id=1)
servo = Servo(26)
angles = []
all_angles = []

servo.move(0)

# Lee el .csv
filepath = "/generated_paths/random_angles.csv"
with open(filepath, "r") as file:
    for line in file:
        angles = [float(x) for x in line.strip().split(",")]
        all_angles.append(angles)

print(f"Loaded {len(all_angles)} angle pairs")
print("Starting random iteration... (Press Ctrl+C to stop)")

# Iterate randomly forever
iteration = 0
try:
    while True:
        # Pick a random angle pair
        t1, t2 = random.choice(all_angles)

        iteration += 1
        print(f"[{iteration}] Moving to: {t1:.1f}°, {t2:.1f}°")

        s1.target_deg(t1)
        s2.target_deg(t2)
        time.sleep(1)

        servo.move(190)
        time.sleep(1)

        servo.move(0)
        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"\nStopped after {iteration} iterations")
    s1.stop()
    s2.stop()
    servo.move(0)
