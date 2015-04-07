import base64
import os
import platform
import subprocess


CALLABLES = {
    # Pi-specific, "faked" OBD data sources
    0xFF: {
        # Pi CPU temperature
        0x00: lambda iface: (
            None
            if platform.platform() != 'Linux'
            else subprocess.check_output(
                '/usr/bin/vcgencmd measure_temp', shell=True
            ).split('=')[1]
        ),
        # Random number generator
        0xFE: lambda iface: base64.b64encode(os.urandom(16)),
        # AT mode echo the version, a good comms test
        0xFF: lambda iface: iface.get('ATI', str_response=True),
    },
}
