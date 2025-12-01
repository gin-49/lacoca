# Code for ESP32 - Dual Stepper with PID Control
from stepper import Stepper
from servo import Servo
from pid import PID
import time

# --- Configuration ---
STEPS_PER_REV = 3200
MAX_SPEED = 2000  # Max steps per second
MIN_SPEED = 500  # Min steps per second
dt = 0.5  # 10ms update interval (100 Hz)

# --- Setup Steppers ---
s1 = Stepper(16, 17, steps_per_rev=STEPS_PER_REV, speed_sps=MIN_SPEED, timer_id=0)
s2 = Stepper(18, 19, steps_per_rev=STEPS_PER_REV, speed_sps=MIN_SPEED, timer_id=1)

# --- Setup PID Controllers ---
# PID controls speed to reach target positions smoothly
pid1 = PID(
    Kp=2.0,  # Proportional gain
    Ki=0.3,  # Integral gain
    Kd=0.1,  # Derivative gain
    setpoint=0,  # Will be updated with target position
    sample_time=dt,  # Match our update rate
    output_limits=(-MAX_SPEED, MAX_SPEED),  # Speed limits
    auto_mode=True,
)

pid2 = PID(
    Kp=2.0,
    Ki=0.3,
    Kd=0.1,
    setpoint=0,
    sample_time=dt,
    output_limits=(-MAX_SPEED, MAX_SPEED),
    auto_mode=True,
)

# --- Setup Servo ---
servo = Servo(26)
servo.move(0)

# --- Read CSV File ---
angles = []
all_angles = []

filepath = "/generated_paths/triangulo_angles.csv"
with open(filepath, "r") as file:
    for line in file:
        angles = [float(x) for x in line.strip().split(",")]
        all_angles.append(angles)

print(f"Loaded {len(all_angles)} angle pairs from CSV")


def move_to_angles_pid(target_deg1, target_deg2, tolerance=0.5):
    """
    Move both steppers to target angles using PID control

    Args:
        target_deg1: Target angle for stepper 1 (degrees)
        target_deg2: Target angle for stepper 2 (degrees)
        tolerance: Position tolerance in degrees
    """
    # Convert degrees to steps
    target_steps1 = int(target_deg1 * STEPS_PER_REV / 360.0)
    target_steps2 = int(target_deg2 * STEPS_PER_REV / 360.0)

    # Set PID setpoints to target positions
    pid1.setpoint = target_steps1
    pid2.setpoint = target_steps2

    # Reset PID controllers for new movement
    pid1.reset()
    pid2.reset()

    # Set stepper targets and start tracking
    s1.target(target_steps1)
    s2.target(target_steps2)
    s1.track_target()
    s2.track_target()

    # Control loop
    while True:
        # Get current positions
        pos1 = s1.get_pos()
        pos2 = s2.get_pos()

        # Calculate errors in steps
        error1 = abs(target_steps1 - pos1)
        error2 = abs(target_steps2 - pos2)

        # Check if both motors reached target
        tolerance_steps = int(tolerance * STEPS_PER_REV / 360.0)
        if error1 < tolerance_steps and error2 < tolerance_steps:
            break

        # PID computes desired speed based on position error
        speed1 = pid1(pos1, dt=dt)
        speed2 = pid2(pos2, dt=dt)

        # Apply speed limits
        speed1 = max(MIN_SPEED, min(abs(speed1), MAX_SPEED))
        speed2 = max(MIN_SPEED, min(abs(speed2), MAX_SPEED))

        # Update stepper speeds
        s1.speed(int(speed1))
        s2.speed(int(speed2))

        # Small delay for control loop timing
        time.sleep(dt)

    # Don't stop motors - just let them coast at the target
    # s1.stop()
    # s2.stop()


def move_to_angles_simple(target_deg1, target_deg2, speed_sps=1000):
    """
    Simple movement without PID (your original approach but waits for completion)

    Args:
        target_deg1: Target angle for stepper 1
        target_deg2: Target angle for stepper 2
        speed_sps: Speed in steps per second
    """
    s1.speed(speed_sps)
    s2.speed(speed_sps)

    s1.target_deg(target_deg1)
    s2.target_deg(target_deg2)

    # Only call track_target if not already running
    if not s1.timer_is_running:
        s1.track_target()
    if not s2.timer_is_running:
        s2.track_target()

    # Wait until both reach target
    while not (s1.is_target_reached() and s2.is_target_reached()):
        time.sleep(0.01)


# --- Main Execution Loop ---
print("Starting motion sequence...")
print(f"Current positions - S1: {s1.get_pos_deg():.2f}°, S2: {s2.get_pos_deg():.2f}°")

# Choose control method:
USE_PID = True  # Set to False for simple control

for i, (t1, t2) in enumerate(all_angles):
    print(f"[{i + 1}/{len(all_angles)}] Moving to: S1={t1:.2f}°, S2={t2:.2f}°")

    if USE_PID:
        # PID-controlled smooth motion
        move_to_angles_pid(t1, t2, tolerance=0.5)
    else:
        # Simple constant-speed motion
        move_to_angles_simple(t1, t2, speed_sps=1000)

    # Optional: small pause between moves
    time.sleep(0.05)

    # Print actual positions
    actual1 = s1.get_pos_deg()
    actual2 = s2.get_pos_deg()
    print(f"  Reached: S1={actual1:.2f}°, S2={actual2:.2f}°")

print("Motion sequence complete!")
print(f"Final positions - S1: {s1.get_pos_deg():.2f}°, S2: {s2.get_pos_deg():.2f}°")

# Cleanup
s1.stop()
s2.stop()
servo.move(0)
