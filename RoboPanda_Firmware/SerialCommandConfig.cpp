#include "RoboPanda_Firmware.h"
#include "RoboPanda_ArduinoMega.h"
#include "SerialCommand.h"
#include "SerialCommandConfig.h"

SerialCommand sCmd;
void SerialInit(){
  Serial.begin(SERIAL_BAUDRATE);
  // Setup callbacks for SerialCommand commands
  sCmd.addCommand("ON",    LED_on);          // Turns LED on
  sCmd.addCommand("OFF",   LED_off);         // Turns LED off
  sCmd.setDefaultHandler(unrecognized);      // Handler for unrecognized commands
  Serial.println("Ready");
}

