#include "CustomServo.h"          // include the custom servo library to use RoboPanda motor/potentiometer as a servo
#include "RoboPanda_ArduinoMega.h";

int headlr_pos;                                                       // HEAD-LR Position
CServo headlr(headl_out,headr_out,HEADLR_PIN);                        // initialize headlr servo

int headud_pos;                                                       // HEAD-LR Position
CServo headud(headu_out,headd_out,HEADUD_PIN);                        // initialize headud servo

int leg_rightfb_pos;                                                  // R-LEG-FB Position
CServo leg_rightfb(leg_rightf_out,leg_rightb_out,LEG_RIGHTFB_PIN);    // initialize leg_rightfb servo

int leg_leftfb_pos;                                                   // L-LEG-FB Position
CServo leg_leftfb(leg_leftf_out,leg_leftb_out,LEG_LEFTFB_PIN);        // initialize leg_leftfb servo

int arm_leftoc_pos;                                                   // L-ARM-OC Position
CServo arm_leftoc(arm_lefto_out,arm_lefto_out,ARM_LEFTOC_PIN);        // initialize arm_leftoc servo

int hand_leftud_pos;                                                  // L-HAND-UD Position
CServo hand_leftud(hand_leftu_out,hand_leftd_out,HAND_LEFTUD_PIN);    // initialize hand_leftud servo

int arm_rightoc_pos;                                                  // R-ARM-OC Position
CServo arm_rightoc(arm_righto_out,arm_righto_out,ARM_RIGHTOC_PIN);    // initialize arm_rightoc servo

int hand_rightud_pos;                                                 // L-HAND-UD Position
CServo hand_rightud(hand_rightu_out,hand_rightd_out,HAND_RIGHTUD_PIN);// initialize hand_rightud servo




