###############################
# RoboPanda Arduino Mega pinout
###############################
Configuration = {
    'HEAD_X': {
        'type': 'RoboPandaServo',
        'description': 'Head Left/Right',
        'digital_pin1': 36,
        'digital_pin2': 37,
        'analog_pin': 3,
        'min' : 343,
        'max' : 650,
    },
    'HEAD_Y': {
        'type': 'RoboPandaServo',
        'description': 'Head Up/Down',
        'digital_pin1': 46,
        'digital_pin2': 47,
        'analog_pin': 7,
        'min' : 348,
        'max' : 593,
    },
    'EyeBrow': {
        'type': 'limit_motor',
        'description': 'Eyebrow Up/Down',
        'digital_pin1': 34,
        'digital_pin2': 35,
        'digital_pin1_switch': 25,
        'digital_pin2_switch': 24
    },
    'Accelerometer': {
        'type': 'accelerometer',
        'description': 'Accelerometer',
        'ACCELEROMETER_X_PIN': 5,
        'ACCELEROMETER_Y_PIN': 4,
        'CART_SW_PIN': 27,
        'BALL_SW_PIN': 26
    },
    'Led': {
        'type': 'led',
        'description': 'LEDs',
        'EYE_LEFT_LED_OUT': 31,
        'EYE_RIGHT_LED_OUT': 30,
        'CHEST_LED_OUT': 2,
        'PALM_LEFT_LED_OUT': 3,
        'PALM_RIGHT_LED_OUT': 4
    },
    'InfrarRed': {
        'type': 'ir',
        'description': 'InfraRed',
        'transmit': 32,
        'receive': 33
    },
    'Ear': {
        'type': 'limit_motor',
        'description': 'Ear Forward/Backward',
        'digital_pin1': 38,
        'digital_pin2': 39,
        'digital_pin1_switch': 29,
        'digital_pin2_switch': 28
    },
    'RightLeg': {
        'type': 'RoboPandaServo',
        'description': 'Right Leg Forward/Backward',
        'digital_pin1': 53,
        'digital_pin2': 52,
        'analog_pin': 6,
        'min' : 350,
        'max' : 550
    },
    'LeftLeg': {
        'type': 'RoboPandaServo',
        'description': 'Left Leg Forward/Backward',
        'digital_pin1': 41,
        'digital_pin2': 40,
        'analog_pin': 2,
        'min' : 350,
        'max' : 550
    },
    'LeftArm': {
        'type': 'RoboPandaServo',
        'description': 'Left Arm Open/Close',
        'digital_pin1': 44,
        'digital_pin2': 45,
        'analog_pin': 1,
        'min' : 350,
        'max' : 550
    },
    'LeftHand': {
        'type': 'RoboPandaServo',
        'description': 'Left Hand Up/Down',
        'digital_pin1': 43,
        'digital_pin2': 42,
        'analog_pin': 8,
        'min' : 350,
        'max' : 550
    },
    'RightArm': {
        'type': 'RoboPandaServo',
        'description': 'Right Arm Open/Close',
        'digital_pin1': 48,
        'digital_pin2': 49,
        'analog_pin': 9,
        'min' : 350,
        'max' : 550
    },
    'RightHand': {
        'type': 'RoboPandaServo',
        'description': 'Right Hand Up/Down',
        'digital_pin1': 51,
        'digital_pin2': 50,
        'analog_pin': 10,
        'min' : 350,
        'max' : 550
    }
}