import numpy as np
from funciones import ik_scara

# Coordenadas xy en csv a una matriz XY a angulos theta


def csv_to_theta(filepath, l1, l2, l5):
    theta = []
    path = np.genfromtxt(filepath, delimiter=",", skip_header=1)

    x_offset = l5 / 2
    y_offset = 100

    for point in path:
        x = point[0] + x_offset
        y = point[1] + y_offset

        ik_result = ik_scara(x, y, l1, l2, l5)
        theta.append(ik_result)
    return theta
