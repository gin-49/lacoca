import struct
import sys

BUF_SIZE = 8
buf = bytearray(BUF_SIZE)
mv = memoryview(buf)


def read_exact(n):
    offs = 0
    while offs < n:
        got = sys.stdin.buffer.readinto(mv[offs:])
        if not got:
            continue
        offs += got


def read_angles():
    """Reads 2 float32 values from USB, returns (t1, t2)."""
    read_exact(BUF_SIZE)
    try:
        return struct.unpack("<ff", buf)
    except Exception:
        return None


def send_ok(t1, t2):
    """Send OK message back to PC."""
    print("OK {:.9f} {:.9f}".format(t1, t2))
