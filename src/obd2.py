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
        # Current KPH
        0x0D: lambda: 100,
    },
}

# Add the extra non-OBD2 mode 0xFF PIDs
MAP.update(extras.MAP)


def value(mode, pid):
    """ Return the value of a mode+pid combination.

        It is up to the lambda in the MAP to do any IO.
    """
    try:
        return MAP[mode][pid]()
    except KeyError:
        return random.randint(0, 255)
