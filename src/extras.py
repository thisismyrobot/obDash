import elm327wifi
import platform
import subprocess


CALLABLES = {
    # Pi-specific, "faked" OBD data sources
    0xFF: {
        # Pi CPU temperature
        0x00: lambda: None
                      if platform.platform() != 'Linux'
                      else subprocess.check_output(
                          '/usr/bin/vcgencmd measure_temp',
                          shell=True).split('=')[1],
        # AT mode echo the version, a good comms test
        0xFF: lambda: elm327wifi.get('ATI', str_response=True),
    },
}
