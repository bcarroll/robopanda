#!/usr/bin/env python3

from webapp import app, logger
from bin.sysinfo import sysinfo_thread
from bin.vision.webstreaming import motion_detection_thread

logger.info("Starting sysinfo_thread")
# Start the sysinfo thread which displays system information on an I2C connected OLED display
sysinfo_thread.start()

logger.info("Starting Motion Detection Thread")
motion_detection_thread.start()

logger.info("Starting RoboPanda Flask webapp")
app.run(host='0.0.0.0', debug=True, threaded=True)
