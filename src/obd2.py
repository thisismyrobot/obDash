import extras
import random


MAP = {
    # Realtime
    0x01: {
        # Block 1 supported PIDs
        0x00: lambda: (0x02, 0x03, 0x05, 0x09),
        # Block 2 supported PIDs
        0x20: lambda: (0x22, 0x23, 0x25),
        # Block 3 supported PIDs
        0x40: lambda: (0x31,),
        # Block 4 supported PIDs
        0x60: lambda: (0x44, 0x46),
        # Current RPM
        0x0C: lambda: random.randint(700, 730),
    },
}
MAP.update(extras.MAP)


def value(mode, pid):
    global MAP
    try:
        return MAP[mode][pid]()
    except KeyError:
        return random.randint(0, 255)
