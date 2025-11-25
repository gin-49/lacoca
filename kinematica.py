import math

# Punto Final
Xc = 15
Yc = 10

# Distancia entre Motores
d = 10.6249

# Links
L1 = 10
L2 = 15
L3 = 15
L4 = 10

# Funcion de kinematica inversa


def parallel_scara_ik(Xc, Yc, d, l1, l2, l3, l4):
    def is_reachable(distance, link1, link2):
        return abs(link1 - link2) <= distance <= (link1 + link2)

    # Posicion de los motores
    m1_x = -d / 2
    m2_x = d / 2

    # Calculate distances from motors to end effector
    c1 = math.sqrt((Xc - m1_x) ** 2 + Yc**2)
    c2 = math.sqrt((Xc - m2_x) ** 2 + Yc**2)

    # Validate reachability using triangle inequality
    if not is_reachable(c1, l1, l2) or not is_reachable(c2, l4, l3):
        return None, None

    try:
        # Calculate angle from motor to end effector
        alpha_approach = math.acos(Xc / c1)
        beta_approach = math.acos((-Xc + m2_x) / c2)

        # Calculate angle contribution from floating link (law of cosines)
        cos_alpha_float = (l2**2 - l1**2 - c1**2) / (-2 * l1 * c1)
        cos_beta_float = (l3**2 - l4**2 - c2**2) / (-2 * l4 * c2)

        # Clamp to valid range to avoid numerical errors
        cos_alpha_float = max(-1.0, min(1.0, cos_alpha_float))
        cos_beta_float = max(-1.0, min(1.0, cos_beta_float))

        alpha_float = math.acos(cos_alpha_float)
        beta_float = math.acos(cos_beta_float)

        # Total motor angles
        alpha_total = alpha_approach + alpha_float
        beta_total = beta_approach + beta_float

        # Convert to degrees
        angle_motor1 = math.degrees(alpha_total)
        angle_motor2 = 180.0 - math.degrees(beta_total)

        return angle_motor1, angle_motor2

    except ValueError:
        # acos argument out of range
        return None, None


# Test
theta1, theta2 = parallel_scara_ik(
    Xc,
    Yc,
    d,
    L1,
    L2,
    L3,
    L4,
)


if theta1 is not None and theta2 is not None:
    print("✓ End effector position is reachable")
    print(f"Left Motor Angle  = {theta1:.4f}°")
    print(f"Right Motor Angle = {theta2:.4f}°")
else:
    print("✗ End effector position is unreachable with current configuration")
    print(f"  Target: ({Xc}, {Yc})")
