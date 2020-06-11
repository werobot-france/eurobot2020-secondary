#!/bin/bash

# Simple bash script to compile and upload code for a specific arduino code

echo "select the arduino ************"
echo "  1) STEPPER ARDUINO"
echo "  2) ENCODER ARDUINO"

arduino="unknown"
port="unknown"

read n
case $n in
  1) echo "Choose stepper arduino..."; arduino="arduino_stepper";; # port="/dev/ttyUSB_NANO_STEPPER";
  2) echo "Choose encoder arduino..."; arduino="arduino_encoder";; # port="/dev/ttyUSB_NANO_ENCODER";
  *) echo "invalid option";;
esac

# take whatever port we have
port=$(ls /dev | grep 'ttyUSB')
port="/dev/$port"

fqbn="arduino:avr:nano:cpu=atmega328old"

echo "Use arduino: $arduino with path: $port "
echo "FQBN: $fqbn"

# copy all file of arduino_commons into the folder

cp ./arduino_commons/* ./$arduino

arduino-cli compile --fqbn $fqbn ./$arduino
echo "> Compiled"
arduino-cli upload --fqbn $fqbn -p /dev/ttyUSB0 ./$arduino
echo "> Uploaded"

rm ./$arduino/SerialProtocol.h
rm ./$arduino/SerialProtocol.cpp

