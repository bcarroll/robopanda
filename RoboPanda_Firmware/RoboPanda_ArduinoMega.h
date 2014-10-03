/*
 *
 * WowWee RoboPanda IO Constants for Arduino Mega
 *
 */
#ifndef RoboPanda_ArduinoMega_h
#define RoboPanda_ArduinoMega_h

#include "CustomServo.h"                  // include the custom servo library to use RoboPanda motor/potentiometer as a servo

#define SERIAL_BAUDRATE 9600              // Serial Port Baudrate
#define SERIAL_BUFFER   16                // bytes to reserve for Serial input data
#define SERIALCOMMAND_BUFFER 32           // Size of the input buffer in bytes (maximum length of one command plus arguments)
#define SERIALCOMMAND_MAXCOMMANDLENGTH 8  // Maximum length of a command excluding the terminating null
//#define SERIALCOMMAND_DEBUG             // Uncomment to run the in debug mode (verbose messages)

// Head Left/Right
#define HEADL_OUT 29                      // HEAD-L OUTPUT PIN
#define HEADR_OUT 27                      // HEAD-R OUTPUT PIN
#define HEADLR_PIN 10                     // HEAD-LR INPUT PIN

// Head Up/Down
#define HEADU_OUT 35                      // HEAD-U OUTPUT PIN
#define HEADD_OUT 37                      // HEAD-D OUTPUT PIN
#define HEADUD_PIN 13                     // HEAD-UD INPUT PIN

// Eyebrow Up/Down
#define EYEBROWU_OUT 33                   // EYEU OUTPUT PIN
#define EYEBROWD_OUT 31                   // EYED OUTPUT PIN
#define EYEBROWU_PIN 41                   // EYEU INPUT PIN (Limit Switch)
#define EYEBROWD_PIN 43                   // EYED INPUT PIN (Limit Switch)

// Accelerometer
#define ACCELEROMETER_X_PIN A9            // TILT_X INPUT PIN
#define ACCELEROMETER_Y_PIN A8            // TILT_Y INPUT PIN

#define CART_SW_PIN 00                    // J15 INPUT PIN
#define BALL_SW_PIN 00                    // Ball Switch INPUT PIN

// LEDs
#define EYE_LEFT_LED_OUT 00               // L-EYE-LED OUTPUT PIN
#define EYE_RIGHT_LED_OUT 00              // R-EYE-LED OUTPUT PIN
#define CHEST_LED_OUT 52                  // FRONT-LED OUTPUT PIN
#define PALM_LEFT_LED_OUT 35              // L-PALM-LED OUTPUT PIN
#define PALM_RIGHT_LED_OUT 00             // R-PALM-LED OUTPUT PIN

// InfraRed
#define IR_TRANS_OUT 00                   // IR_TX OUTPUT PIN
#define IR_RECEIVE_PIN 00                 // IR_RX OUTPUT PIN

// Ear Forward/Backward
#define EARF_OUT 25                       // EAR-F OUTPUT PIN
#define EARB_OUT 23                       // EAR-B OUTPUT PIN
#define EARU_PIN 37                       // EARU INPUT PIN
#define EARD_PIN 39                       // EARD INPUT PIN

// Right Leg Forward/Backward
#define LEG_RIGHTF_OUT 22                 // R-LEG-F OUTPUT PIN
#define LEG_RIGHTB_OUT 24                 // R-LEG-B OUTPUT PIN
#define LEG_RIGHTFB_PIN 15                // R-LEG-FB INPUT PIN

// Left Leg Forward/Backward
#define LEG_LEFTF_OUT 47                  // L-LEG-F OUTPUT PIN
#define LEG_LEFTB_OUT 49                  // L-LEG-B OUTPUT PIN
#define LEG_LEFTFB_PIN 14                 // L-LEG-FB INPUT PIN

// Left Arm Open/Close
#define ARM_LEFTO_OUT 41                  // L-ARM-O OUTPUT PIN
#define ARM_LEFTC_OUT 39                  // L-ARM-C OUTPUT PIN
#define ARM_LEFTOC_PIN 12                 // L-ARM-OC INPUT PIN

// Left Hand Up/Down
#define HAND_LEFTU_OUT 43                 // L-HAND-U OUTPUT PIN
#define HAND_LEFTD_OUT 45                 // L-HAND-D OUTPUT PIN
#define HAND_LEFTUD_PIN 11                // L-HAND-UD INPUT PIN

// Right Arm Open/Close
#define ARM_RIGHTO_OUT 31                 // R-ARM-O OUTPUT PIN
#define ARM_RIGHTC_OUT 33                 // R-ARM-C OUTPUT PIN
#define ARM_RIGHTOC_PIN 6                 // R-ARM-OC INPUT PIN

// Right Hand Up/Down
#define HAND_RIGHTU_OUT 27                // R-HAND-U OUTPUT PIN
#define HAND_RIGHTD_OUT 29                // R-HAND-D OUTPUT PIN
#define HAND_RIGHTUD_PIN 7                // R-HAND-OC INPUT PIN

#endif
