import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import interp1d

# ------------------------------
# 1️⃣ Robot parameters
# ------------------------------
AB = 0.15
BC = 0.15
DC = 0.15
ED = 0.15

steps_per_rev = 200
microsteps = 16
max_speed = 700  # steps/s

# ------------------------------
# 2️⃣ Kinematics functions
# ------------------------------


def inverse_kinematics(Px, Py, Ex, Ey):
    AC = np.sqrt(Px**2 + Py**2)
    alpha1 = np.arctan2(Py, Px)
    Beta1 = np.arccos(np.clip((AC**2 + AB**2 - BC**2)/(2*AC*AB), -1, 1))
    theta1 = alpha1 + Beta1
    Bx = AB*np.cos(theta1)
    By = AB*np.sin(theta1)

    EC = np.sqrt((Ex-Px)**2 + (Ey-Py)**2)
    alpha2 = np.arctan2(Py, Ex-Px)
    Beta2 = np.arccos(np.clip((EC**2 + ED**2 - DC**2)/(2*EC*ED), -1, 1))
    theta2 = np.pi - alpha2 - Beta2
    Dx = Ex + ED*np.cos(theta2)
    Dy = ED*np.sin(theta2)

    return Bx, By, Dx, Dy, theta1, theta2


def solve_C(Bx, By, Dx, Dy):
    r = np.sqrt((Dx-Bx)**2 + (Dy-By)**2)
    a, b, c = BC, DC, r
    if c > a+b or c < abs(a-b):
        return None
    cos_gamma = np.clip((a**2 + c**2 - b**2)/(2*a*c), -1, 1)
    gamma = np.arccos(cos_gamma)
    phi = np.arctan2(Dy-By, Dx-Bx)
    Cx1 = Bx + a*np.cos(phi+gamma)
    Cy1 = By + a*np.sin(phi+gamma)
    Cx2 = Bx + a*np.cos(phi-gamma)
    Cy2 = By + a*np.sin(phi-gamma)
    return (Cx1, Cy1) if Cy1 > Cy2 else (Cx2, Cy2)


def check_singularity(Bx, By, Cx, Cy, Dx, Dy):
    def slope(p1, p2):
        if p2[0]-p1[0] == 0:
            return np.inf
        return (p2[1]-p1[1])/(p2[0]-p1[0])
    s1 = slope((Bx, By), (Cx, Cy))
    s2 = slope((Cx, Cy), (Dx, Dy))
    return np.isclose(s1, s2, atol=1e-3)


def angle_to_steps(theta_rad):
    total_steps = steps_per_rev * microsteps
    theta_deg = np.degrees(theta_rad)
    return int(np.round(theta_deg/360*total_steps))


# ------------------------------
# 3️⃣ Define square corners
# ------------------------------
square_corners = np.array([
    [0.05, 0.15],
    [0.05, 0.20],
    [0.10, 0.20],
    [0.10, 0.15],
    [0.05, 0.15]  # close the square
])

# Interpolate path
num_points = 200
t_orig = np.linspace(0, 1, len(square_corners))
t_dense = np.linspace(0, 1, num_points)
interp_x = interp1d(t_orig, square_corners[:, 0], kind='linear')
interp_y = interp1d(t_orig, square_corners[:, 1], kind='linear')
Px_points = interp_x(t_dense)
Py_points = interp_y(t_dense)

Ex, Ey = 0.10625, 0
delta_t = 0.05  # initial time step (s)

# ------------------------------
# 4️⃣ Compute trajectory
# ------------------------------
vPx, vPy, vBx, vBy, vCx, vCy, vDx, vDy = [], [], [], [], [], [], [], []
vTheta1, vTheta2 = [], []
vMotor1Steps, vMotor2Steps = [], []
motor_speeds1, motor_speeds2 = [], []
singularities = []

for i, (Px, Py) in enumerate(zip(Px_points, Py_points)):
    Bx, By, Dx, Dy, theta1, theta2 = inverse_kinematics(Px, Py, Ex, Ey)
    C = solve_C(Bx, By, Dx, Dy)
    if C is None:
        continue
    Cx, Cy = C

    vPx.append(Px)
    vPy.append(Py)
    vBx.append(Bx)
    vBy.append(By)
    vCx.append(Cx)
    vCy.append(Cy)
    vDx.append(Dx)
    vDy.append(Dy)
    vTheta1.append(theta1)
    vTheta2.append(theta2)
    vMotor1Steps.append(angle_to_steps(theta1))
    vMotor2Steps.append(angle_to_steps(theta2))
    singularities.append(check_singularity(Bx, By, Cx, Cy, Dx, Dy))

# Compute speeds
motor_speeds1 = [0]
motor_speeds2 = [0]
for i in range(1, len(vMotor1Steps)):
    s1 = (vMotor1Steps[i]-vMotor1Steps[i-1])/delta_t
    s2 = (vMotor2Steps[i]-vMotor2Steps[i-1])/delta_t
    motor_speeds1.append(s1)
    motor_speeds2.append(s2)

# Scale delta_t if needed
max_required_speed = max(np.max(np.abs(motor_speeds1)),
                         np.max(np.abs(motor_speeds2)))
if max_required_speed > max_speed:
    scale_factor = max_required_speed / max_speed
    delta_t *= scale_factor
    print(f"Scaling delta_t by {scale_factor:.2f} to respect max_speed")
    motor_speeds1 = [0]
    motor_speeds2 = [0]
    for i in range(1, len(vMotor1Steps)):
        s1 = (vMotor1Steps[i]-vMotor1Steps[i-1])/delta_t
        s2 = (vMotor2Steps[i]-vMotor2Steps[i-1])/delta_t
        motor_speeds1.append(s1)
        motor_speeds2.append(s2)

# ------------------------------
# 5️⃣ Animation
# ------------------------------
fig, ax = plt.subplots()
ax.set_xlim(-0.1, 0.20)
ax.set_ylim(-0.1, 0.25)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title("5-Bar Robot Square Path")
ax.grid(True)

line, = ax.plot([], [], "-o", lw=2, markersize=5)
trace, = ax.plot([], [], ".g")
angle_text = ax.text(0.02, 0.205, "", transform=ax.transData)


def update(frame):
    Bx, By = vBx[frame], vBy[frame]
    Cx, Cy = vCx[frame], vCy[frame]
    Dx, Dy = vDx[frame], vDy[frame]
    Ax, Ay = 0, 0

    x_coords = [Ax, Bx, Cx, Dx, Ex]
    y_coords = [Ay, By, Cy, Dy, Ey]

    color = 'r' if singularities[frame] else 'b'
    line.set_data(x_coords, y_coords)
    line.set_color(color)
    trace.set_data(vPx[:frame+1], vPy[:frame+1])

    theta1_deg = np.degrees(vTheta1[frame])
    theta2_deg = np.degrees(vTheta2[frame])
    angle_text.set_text(f"θ1={theta1_deg:.1f}°  θ2={theta2_deg:.1f}°")

    return line, trace, angle_text


ani = FuncAnimation(fig, update, frames=len(
    vPx), interval=delta_t*1000, blit=True)
plt.show()

# ------------------------------
# 6️⃣ Print motor info
# ------------------------------
for i in range(len(vMotor1Steps)):
    print(f"Step {i}: θ1={np.degrees(vTheta1[i]):.2f}°, θ2={np.degrees(vTheta2[i]):.2f}°, "
          f"Motor1={vMotor1Steps[i]} steps, Motor2={vMotor2Steps[i]} steps, "
          f"Speed1={motor_speeds1[i]:.1f} steps/s, Speed2={motor_speeds2[i]:.1f} steps/s")
