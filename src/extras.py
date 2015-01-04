import subprocess


MAP = {
    # Pi-specific, "faked" OBD data sources
    0xFF: {
        # Pi CPU temperature
        0x00: lambda: subprocess.check_output(
            'vcgencmd measure_temp'
        ).split('=')[1],
    },
}
