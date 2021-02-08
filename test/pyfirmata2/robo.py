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


###############################
# RoboPanda Arduino Mega pinout
###############################
# BAUDRATE=57600
# HEADL_OUT=36
# HEADR_OUT=37
# HEADLR_PIN=6
# HEADU_OUT=46
# HEADD_OUT=47
# HEADUD_PIN=7
# EYEBROWU_OUT=34
# EYEBROWD_OUT=35
# EYEBROWU_PIN=25
# EYEBROWD_PIN=24
# ACCELEROMETER_X_PIN=5
# ACCELEROMETER_Y_PIN=4
# CART_SW_PIN=27
# BALL_SW_PIN=26
# EYE_LEFT_LED_OUT=31
# EYE_RIGHT_LED_OUT=30
# CHEST_LED_OUT=2
# PALM_LEFT_LED_OUT=3
# PALM_RIGHT_LED_OUT=4
# IR_TRANS_OUT=32
# IR_RECEIVE_PIN=33
# EARF_OUT=38
# EARB_OUT=39
# EARU_PIN=29
# EARD_PIN=28
# LEG_RIGHTF_OUT=53
# LEG_RIGHTB_OUT=52
# LEG_RIGHTFB_PIN=3
# LEG_LEFTF_OUT=41
# LEG_LEFTB_OUT=40
# LEG_LEFTFB_PIN=2
# ARM_LEFTO_OUT=44
# ARM_LEFTC_OUT=45
# ARM_LEFTOC_PIN=1
# HAND_LEFTU_OUT=43
# HAND_LEFTD_OUT=42
# HAND_LEFTUD_PIN=8
# ARM_RIGHTO_OUT=48
# ARM_RIGHTC_OUT=49
# ARM_RIGHTOC_PIN=9
# HAND_RIGHTU_OUT=51
# HAND_RIGHTD_OUT=50
# HAND_RIGHTUD_PIN=10