""" Module to handle the OBD2 protocol.

    Is used by the obd2_proc sub-process, and each call to the "value" method
    is passed the external interface.
"""
import obdash.extras


# Maps MODE and PID to a callable
CALLABLES = {
    # Realtime
    0x01: {
        # Block 1 supported PIDs
        0x00: lambda iface: (0x02, 0x03, 0x05, 0x09),
        # Block 2 supported PIDs
        0x20: lambda iface: (0x22, 0x23, 0x25),
        # Block 3 supported PIDs
        0x40: lambda iface: (0x31,),
        # Block 4 supported PIDs
        0x60: lambda iface: (0x44, 0x46),
        # Current RPM
        0x0C: lambda iface: iface.get('010C'),
        # Current KPH
        0x0D: lambda iface: iface.get('010D'),
        # Current Intake Air Temperature
        0x0F: lambda iface: iface.get('010F'),
    },
}

# Add the extra non-OBD2 mode 0xFF PIDs
CALLABLES.update(obdash.extras.CALLABLES)

# Processors for anything that cannot just be returned as-is.
PROCESSORS = {
    0x01: {
        # Current RPM
        0x0C: lambda a, b: ((a * 256) + b) / 4,
        # Intake Air Temperature
        0x0F: lambda a: a - 40,
    }
}


def value(iface, mode, pid):
    """ Return the value of a mode+pid combination.

        It is up to the lambda in the CALLABLES dict to do any IO.
    """
    # Retrieve a function to get the values for a mode + pid combination.
    value_getter_func = CALLABLES[mode][pid]

    # Attempt to get the values using that function and the OBD2 interface
    # module.
    values = value_getter_func(iface)

    try:
        # Attempt to process the values and return the processed result
        return PROCESSORS[mode][pid](*values)

    except KeyError:
        # Not all mode + pid combinations need a processor, so this
        # exception is not a problem.
        pass

    return values
