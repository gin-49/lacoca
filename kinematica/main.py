import matplotlib as plt
import numpy as np
import pandas as pd

# 1) Import path
path = "./paths/test.csv"

df = pd.read_csv(path)
x_path = df["x"].to_list()
y_path = df["y"].to_list()

# 2) Robot parameters

L1 = 0.1
L2 = 0.15
L3 = 0.15
L4 = 0.1

d = 106.249  # Distancia entre centros

resolution = 3600  # Pasos por 360

# 3) Inverse Kinematics


def inverse_kinematics(Xc, Yc, l1, l2, l3, l4, d):
