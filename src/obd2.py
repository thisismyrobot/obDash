import random


MAP = {
    0x01: {
        # Block 0 supported PIDs
        0x00: lambda resp: (0x02, 0x03, 0x05, 0x09)  # Example response
    },
}


def value(mode, pid):
    global MAP
    try:
        return MAP[mode][pid](None)  # None to become result from serial dev.
    except KeyError:
        return random.randint(0, 255)
