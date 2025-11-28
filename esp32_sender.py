import serial
import struct
import time


class ESP32Sender:
    def __init__(self, port="/dev/ttyUSB0", baud=115200, timeout=1):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        time.sleep(2)  # wait for ESP32 reset

    def send_angles(self, t1, t2):
        """Send two float32 angles as binary packet."""
        packet = struct.pack("<ff", float(t1), float(t2))  # little-endian
        self.ser.write(packet)

    def read_reply(self):
        """Read text reply from ESP32 (like 'OK t1 t2')."""
        line = self.ser.readline().decode(errors="ignore").strip()
        return line

    def close(self):
        self.ser.close()
