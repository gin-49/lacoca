import numpy as np
import matplotlib.pyplot as plt
from functions import fk_scara


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
        f"X range: [{workspace_points[:, 0].min():.2f}, {workspace_points[:, 0].max():.2f}]"
    )
    print(
        f"Y range: [{workspace_points[:, 1].min():.2f}, {workspace_points[:, 1].max():.2f}]"
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


# Example usage
if __name__ == "__main__":
    l1, l2, l5 = 100, 150, 106.249
    plot_scara_workspace(
        l1, l2, l5, theta1_range=(0, 130), theta2_range=(0, 130), resolution=1000
    )
