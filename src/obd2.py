import random


MAP = {
    0x01: {
        # Block 1 supported PIDs
        0x00: lambda resp: (0x02, 0x03, 0x05, 0x09),
        # Block 2 supported PIDs
        0x20: lambda resp: (0x22, 0x23, 0x25),
        # Block 3 supported PIDs
        0x40: lambda resp: (0x31,),
        # Block 4 supported PIDs
        0x60: lambda resp: (0x44, 0x46),
        # Current RPM
        0x0C: lambda resp: random.randint(700, 730),
    },
}


def value(mode, pid):
    global MAP
    try:
        return MAP[mode][pid](None)  # None to become result from serial dev.
    except KeyError:
        return random.randint(0, 255)
