import math

# Funcion para el calculo de la kinematica inversa del scara


def ik_scara(Xc, Yc, d, l1, l2, l3, l4):
    # Ubicacion de los motores
    m1 = -d / 2  # Izquierdo
    m2 = d / 2  # Derecho

    try:
        # Distancia punto a punto
        pp1 = math.sqrt((m1 - Xc) ** 2 + (Yc) ** 2)
        pp2 = math.sqrt((m2 - Xc) ** 2 + (Yc) ** 2)

        # Angulos internos del motor izquierdo
        alpha1 = math.acos((l1**2 - l2**2 + pp1) / (2 * l1 * math.sqrt(pp1)))
        beta1 = math.atan2(Yc, Xc)

        # Angulos internos del motor derecho
        alpha2 = math.acos((l4**2 - l3**2 + pp2) / (2 * l4 * math.sqrt(pp2)))
        beta2 = math.atan2(Yc, Xc + d)

        # Suma de alpha y beta ajustando para el angulo del paso a paso
        theta1 = math.degrees(alpha1 + beta1) - 90
        theta2 = math.degrees(alpha2 + beta2) - 90

        if alpha1 and beta2 > 0:
            return theta1, theta2
        else:
            return None, None

    # Manejo de Errores
    except ValueError:
        return None, None


# TEST

xc = 10
yc = 10
d = 106.249
l1 = 10
l2 = 15
l3 = 15
l4 = 10

path = ik_scara(xc, yc, d, l1, l2, l3, l4)

print(path)
