import sys
import logging
from config import Configuration
from pyfirmata import ArduinoMega, util
from time import sleep

class RoboPanda():
    port = {}
    def __init__(self):
        logging.info('Initializing RoboPanda...')
        self.panda = ArduinoMega('/dev/ttyACM0')
        if self.panda.name:
            logging.info('Connected to RoboPanda on %s' % self.panda.name)
        else:
            logging.error('Error connecting to RoboPanda')
        it = util.Iterator(self.panda)
        it.start()
        for key in Configuration:
            if key.endswith('analog_pin'):
                rkey = key.replace('_analog_pin', '')
                logging.debug('Initializing %s [A%s]' % (rkey, str(Configuration[key])))
                self.port[rkey] = {}
                self.port[rkey]['port'] = self.panda.get_pin('a:' + str(Configuration[key]) + ':i')
                self.port[rkey]['pin'] = 'A%s' % str(Configuration[key])
                self.port[rkey]['min'] = Configuration[rkey + '_min']
                self.port[rkey]['max'] = Configuration[rkey + '_max']
                self.val(rkey) # Get initial value from port to make sure it is alive... not sure why this is needed, but without it the first several values are None

    def shutdown(self):
        self.panda.shutdown()

    def map_range(value, range1Min, range1Max, range2Min, range2Max):
        # Determine the 'width' of each range
        range1 = range1Max - range1Min
        range2 = range2Max - range2Min
        # Map range1 into a 0-1 range (float)
        mappedValue = float(value - range1Min) / float(range1)
        # Convert the 0-1 range into a value in range2
        return range2Min + (mappedValue * range2)

    def val(self, port_name):
        value = None
        loop  = 0
        while loop < 5:
            try:
                value = self.port[port_name]['port'].value
                if value is not None:
                    return value
                else:
                    logging.debug('%s value returned None [%s] retrying' % (str(port_name), str(loop)))
                loop += 1
                sleep(.1)
            except:
                pass
        return value

    def read(self, port_name):
        value = None
        loop  = 0
        while loop < 5:
            try:
                value = self.port[port_name]['port'].read()
                if value is not None:
                    return value
                else:
                    logging.debug('%s value returned None [%s] retrying' % (str(port_name), str(loop)))
                loop += 1
                sleep(.1)
            except:
                pass
        return value


    def debug(self):
        for port in self.port:
            logging.debug('Port: %s (min: %s - max: %s) [%s]' % (port, self.port[port]['min'], self.port[port]['max'], self.val(port)))


#try:
#    while True:
#        time.sleep(.1)
#        value, time_stamp = board.analog_read(pin)
#except KeyboardInterrupt:
#    my_board.shutdown()
#    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    panda = RoboPanda()
    try:
        while True:
            panda.debug()
            sleep(1)
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