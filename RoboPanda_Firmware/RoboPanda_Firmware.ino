/*
 * WowWee RoboPanda toy robot Arduino Mega firmware
 */

#include "Arduino.h"
#include "RoboPanda_Firmware.h"
#include "RoboPanda_ArduinoMega.h"
#include "SerialCommandConfig.h"

void setup() {
  pinMode(arduinoLED, OUTPUT);      // Configure the onboard LED for output
  digitalWrite(arduinoLED, LOW);    // default to LED off
  SerialInit();
}

void loop() {
}

void LED_on() {
  Serial.println("LED on");
  digitalWrite(arduinoLED, HIGH);
}

void LED_off() {
  Serial.println("LED off");
  digitalWrite(arduinoLED, LOW);
}

void unrecognized(const char *command) {
  Serial.println("UnrecognizedCommand");
}

