import math
import numpy as np
import matplotlib.pyplot as plt

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

    # Usually we choose the "elbow-up"
    return round(Cx_up, 2), round(Cy_up, 2)


def plot_scara_workspace(
    l1, l2, l5, theta1_range=(0, 180), theta2_range=(0, 180), resolution=50
):
    """
    Plot workspace of a planar parallel SCARA robot using fk_scara function.

    Parameters:
    - l1: length of driven links
    - l2: length of floating links
    - l5: distance between driven joints (base separation)
    - theta1_range: tuple (min_angle, max_angle) in degrees for left joint (default: (0, 180))
    - theta2_range: tuple (min_angle, max_angle) in degrees for right joint (default: (0, 180))
    - resolution: number of samples per joint (default: 50)
    """

    workspace_points = []
    theta1_samples = np.linspace(theta1_range[0], theta1_range[1], resolution)
    theta2_samples = np.linspace(theta2_range[0], theta2_range[1], resolution)

    for theta1 in theta1_samples:
        for theta2 in theta2_samples:
            coord = fk_scara(theta1, theta2, l1, l2, l5)
            if coord is not None:
                workspace_points.append(coord)

    workspace_points = np.array(workspace_points)

    if len(workspace_points) == 0:
        print("No valid workspace points found!")
        return

    print(f"Workspace points: {len(workspace_points)}")
    print(
        f"X range: [{workspace_points[:, 0].min():.2f}, {
            workspace_points[:, 0].max():.2f}]"
    )
    print(
        f"Y range: [{workspace_points[:, 1].min():.2f}, {
            workspace_points[:, 1].max():.2f}]"
    )

    # Plot workspace
    plt.figure(figsize=(10, 10))
    plt.scatter(workspace_points[:, 0], workspace_points[:, 1], s=10, alpha=0.6)
    plt.plot([0, l5], [0, 0], "ro", markersize=8, label="Base joints")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title(f"Parallel SCARA Robot Workspace (l1={l1}, l2={l2}, l5={l5})")
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
