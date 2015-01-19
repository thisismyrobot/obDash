import platform
import subprocess


MAP = {
    # Pi-specific, "faked" OBD data sources
    0xFF: {
        # Pi CPU temperature
        0x00: lambda: None
                      if platform.platform() != 'Linux'
                      else subprocess.check_output(
                          '/usr/bin/vcgencmd measure_temp',
                          shell=True).split('=')[1],
    },
}
