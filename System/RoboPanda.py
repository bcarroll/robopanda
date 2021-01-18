#!/usr/bin/env python3

from webapp import webapp
from bin.sysinfo import sysinfo_thread

# Start the sysinfo thread which displays system information on an I2C connected OLED display
sysinfo_thread.start()

webapp.run(host='0.0.0.0', port=80, debug=True)
