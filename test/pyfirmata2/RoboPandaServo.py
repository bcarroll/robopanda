from time import sleep
class RoboPandaServo():
    def __init__(self, board, analog_pin, digital_pin1, digital_pin2, min_val, max_val, name=None, initialize_loop=5, initialize_delay=.1):
        """
        RoboPandaServo object constructor

        :param board: pyfirmata object
        :param analog_pin: Analog pin number (middle wire of the potentiometer attached to the motor)
        :param digital_pin1: Digital pin number which controls motor direction 1 (direction of min)
        :param digital_pin2: Digital pin number which controls motor direction 2 (direction of max)
        """
        self.analog_pin       = analog_pin
        self.digital1         = digital_pin1
        self.digital2         = digital_pin2
        self.min              = min_val
        self.max              = max_val
        self.analog           = board.get_pin('a:' + str(self.analog_pin) + ':i')
        self.dirMin           = board.get_pin('d:' + str(self.digital1) + ':o')
        self.dirMax           = board.get_pin('d:' + str(self.digital2) + ':o')
        self.initialize_loop  = initialize_loop
        self.initialize_delay = initialize_delay
        if name is not None:
            self.name = name
        else:
            self.name = 'A' + analog_pin

    def position(self):
        """ Get the current position (0-100) of the RoboPanda "Servo" motor """
        try:
            return ( (self.val() - self.min) / (self.max - self.min) ) * 100
        except ZeroDivisionError as zde:
            logging.error('Unable to get position of %s.  Verify the min and max values in config.py' % self.name)

    def val(self):
        """ Get the current value of the analog_pin """
        # This is done via a loop in-case the value is not available on the first request (seems to take at least 1 iteration the first time through)
        value = None
        loop  = 0
        while loop < self.initialize_loop:
            try:
                value = int(self.analog.value * 1000)
                if value is not None:
                    return value
                else:
                    logging.debug('%s.value returned None [%s] retrying' % (str(self.name), str(loop)))
                loop += 1
                sleep(self.initialize_delay)
            except:
                pass
        return value

    def moveTo(self, position):
        if self.position() < position:
            while self.position() != position and self.position() > self.min and self.position() < self.max:
                self.dirMax.write(1)
                sleep(.01)
            self.dirMax.write(0)
        elif self.position() > position:
            while self.position() != position and self.position() > self.min and self.position() < self.max:
                self.dirMin.write(1)
                sleep(.01)
            self.dirMin.write(0)