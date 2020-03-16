echo "COMPILE AND UPLOAD SCRIPT FOR STEPPER"
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old ./arduino_stepper
echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega328old -p /dev/ttyUSB1 ./arduino_stepper
echo "> Uploaded"
