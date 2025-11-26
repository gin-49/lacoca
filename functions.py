import math

# Funcion para el calculo de la kinematica inversa del scara

# TODO Implementar Forward Kinematics para Visualizacion, Transformar SVG a
# CSV y a Angulos, Generar trayectorias, Calculos de Dinamica torque velocidad,etc?, GUI en tkinter


def ik_scara(Xc, Yc, l1, l2, l5):
    # Left arm
    c = math.sqrt(Xc**2 + Yc**2)
    if c > l1 + l2 or c < abs(l1 - l2):
        return None  # Target unreachable
    theta1 = math.atan2(Yc, Xc) + math.acos((l1**2 + c**2 - l2**2) / (2 * l1 * c))

    # Right arm (base at x = l5)
    e = math.sqrt((l5 - Xc) ** 2 + Yc**2)
    if e > l1 + l2 or e < abs(l1 - l2):
        return None  # Target unreachable
    theta2 = math.atan2(Yc, Xc - l5) - math.acos((l1**2 + e**2 - l2**2) / (2 * l1 * e))

    return math.degrees(theta1), math.degrees(theta2)


# TEST
xc = 100
yc = 105
l1 = 100
l2 = 150
l5 = 106.249

ik = ik_scara(xc, yc, l1, l2, l5)
print(ik)
print(xc, yc)
