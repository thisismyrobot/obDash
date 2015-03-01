import elm327wifi
import extras


# Maps MODE and PID to a callable
CALLABLES = {
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
        0x0C: lambda: elm327wifi.get('010C'),
        # Current KPH
        0x0D: lambda: elm327wifi.get('010D'),
    },
}

# Add the extra non-OBD2 mode 0xFF PIDs
CALLABLES.update(extras.CALLABLES)

# Processors for anything that cannot just be returned as-is.
PROCESSORS = {
    0x01: {
        0x0C: lambda a, b: ((a * 256) + b) / 4,
    }
}


def value(mode, pid):
    """ Return the value of a mode+pid combination.

        It is up to the lambda in the MAP to do any IO.
    """
    func = CALLABLES[mode][pid]
    data = func()
    try:
        data = PROCESSORS[mode][pid](*data)
    except KeyError:
        pass
