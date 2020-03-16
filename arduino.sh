#!/bin/bash

# Simple bash script to compile and upload code for a specific arduino code

echo "select the arduino ************"
echo "  1) STEPPER ARDUINO"
echo "  2) ENCODER ARDUINO"

arduino="unknown"
port="unknown"

read n
case $n in
  1) echo "Choose stepper arduino..."; arduino="arduino_stepper"; port="/dev/ttyUSB_NANO_STEPPER";;
  2) echo "Choose encoder arduino..."; arduino="arduino_encoder"; port="/dev/ttyUSB_NANO_ENCODER";;
  *) echo "invalid option";;
esac

echo "Use arduino: $arduino with path: $port "

arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega168 ./$arduino
echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega168 -p /dev/ttyUSB0 ./$arduino
echo "> Uploaded"

