# Genera angulos a un csv para copiarlos en el ESP32
import os
import csv
from trayectoria import csv_to_theta
import time

# Configuración de longitudes
l1 = 100
l2 = 150
l5 = 106.249

# Carpetas
input_folder = "./paths"
output_folder = "./generated_paths"

# Espera inicial
time.sleep(2)

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Iterar sobre todos los archivos CSV de la carpeta de entrada
for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        pathfile = os.path.join(input_folder, file)
        angles = csv_to_theta(pathfile, l1, l2, l5)

        output_file = os.path.join(
            output_folder, f"{os.path.splitext(file)[0]}_angles.csv"
        )
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            for i, (theta1, theta2) in enumerate(angles, start=1):
                t1 = (theta1 - 90) * -1
                t2 = -theta2 + 90

                writer.writerow([t1, t2])

        print(f"Generated {output_file}")
