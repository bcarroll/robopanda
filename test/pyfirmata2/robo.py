import sys
import logging
from config import Configuration
from pyfirmata import ArduinoMega, util
from time import sleep
from RoboPandaServo import RoboPandaServo

class RoboPanda():
    port = {}
    def __init__(self):
        logging.info('Initializing RoboPanda...')
        self.board = ArduinoMega('/dev/ttyACM0')
        if self.board.name:
            logging.info('Connected to RoboPanda on %s' % self.board.name)
        else:
            logging.error('Error connecting to RoboPanda')
        self.it = util.Iterator(self.board)
        self.it.start()
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
