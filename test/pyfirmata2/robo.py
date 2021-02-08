import sys
import logging
from config import Configuration
from pyfirmata import ArduinoMega, util
from time import sleep

class RoboPandaServo():
    def __init__(self, board, analog_pin, digital_pin1, digital_pin2, min_val, max_val, name=None, initialize_loop=5, initialize_delay=.1):
        """
        RoboPandaServo object constructor

        :param board: pyfirmata object
        :param analog_pin: Analog pin number (middle wire of the potentiometer attached to the motor)
        :param digital_pin1: Digital pin number which controls motor direction 1
        :param digital_pin2: Digital pin number which controls motor direction 2
        """
        self.analog           = analog_pin
        self.digital1         = digital_pin1
        self.digital2         = digital_pin2
        self.min              = min_val
        self.max              = max_val
        self.servo            = board.get_pin('a:' + str(self.analog) + ':i')
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
                value = int(self.servo.value * 1000)
                if value is not None:
                    return value
                else:
                    logging.debug('%s.value returned None [%s] retrying' % (str(self.name), str(loop)))
                loop += 1
                sleep(self.initialize_delay)
            except:
                pass
        return value

class RoboPanda():
    port = {}
    def __init__(self):
        logging.info('Initializing RoboPanda...')
        self.board = ArduinoMega('/dev/ttyACM0')
        if self.board.name:
            logging.info('Connected to RoboPanda on %s' % self.board.name)
        else:
            logging.error('Error connecting to RoboPanda')
        it = util.Iterator(self.board)
        it.start()
        for key in Configuration:
            if Configuration[key]['type'] == 'RoboPandaServo':
                logging.debug('Initializing %s [A%s]' % (Configuration[key]['description'], str(Configuration[key]['analog_pin'])))
                self.port[key] = RoboPandaServo(self.board, Configuration[key]['analog_pin'], Configuration[key]['digital_pin1'], Configuration[key]['digital_pin2'], Configuration[key]['min'], Configuration[key]['max'], name=key)
                self.port[key].val()

    def debug(self):
        """ Debug log all ports and values """
        for port in self.port:
            if Configuration[port]['type'] == 'RoboPandaServo':
                logging.debug('Port: %s (min: %s - max: %s) position: %s, val: %s' % (port, self.port[port].min, self.port[port].max, self.port[port].position(), self.port[port].val()))
            else:
                logging.debug('Port: %s not configured' % port)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    panda = RoboPanda()
    it = util.Iterator(panda)
    it.start()
    try:
        while True:
            panda.debug()
            sleep(1)
            logging.debug('\n----------------------------------------------------------------------------\n')
    except KeyboardInterrupt:
        sys.exit(0)
