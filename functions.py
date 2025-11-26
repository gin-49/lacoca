import math

# Funcion para el calculo de la kinematica inversa del scara


def ik_scara(Xc, Yc, l1, l2, l5):
    try:
        c = math.sqrt(Xc**2 + Yc**2)
        if c > l1 + l2 or c < abs(l1 - l2):
            return None  # Target unreachable
        theta1 = math.atan2(Yc, Xc) + math.acos((l1**2 + c**2 - l2**2) / (2 * l1 * c))

        e = math.sqrt((l5 - Xc) ** 2 + Yc**2)
        if e > l1 + l2 or e < abs(l1 - l2):
            return None
        theta2 = math.atan2(Yc, Xc - l5) - math.acos(
            (l1**2 + e**2 - l2**2) / (2 * l1 * e)
        )

        theta1 = round(math.degrees(theta1), 10)
        theta2 = round(math.degrees(theta2), 10)

    except ValueError:
        return "falla de calculo"

    return theta1, theta2


def fk_scara(theta1, theta2, l1, l2, l5):
    # --- Convert to radians ---
    t1 = math.radians(theta1)
    t2 = math.radians(theta2)

    # --- Joint B (left) ---
    Bx = l1 * math.cos(t1)
    By = l1 * math.sin(t1)

    # --- Joint D (right) ---
    Dx = l5 + l1 * math.cos(t2)
    Dy = l1 * math.sin(t2)

    # --- Distance BD ---
    BD = math.sqrt((Dx - Bx) ** 2 + (Dy - By) ** 2)

    # Check reachability
    if BD > 2 * l2:
        return None  # arms cannot meet, impossible configuration

    # --- Midpoint M of BD ---
    Mx = (Bx + Dx) / 2
    My = (By + Dy) / 2

    # --- Distance from midpoint to C ---
    h = math.sqrt(l2**2 - (BD / 2) ** 2)

    # --- Direction perpendicular to BD ---
    ux = -(Dy - By) / BD  # normalized perpendicular
    uy = (Dx - Bx) / BD

    # Two possible solutions: elbow-up or elbow-down
    Cx_up = Mx + h * ux
    Cy_up = My + h * uy

    Cx_down = Mx - h * ux
    Cy_down = My - h * uy

    # Usually we choose the "elbow-up"
    return round(Cx_up, 2), round(Cy_up, 2)
