arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old ./arduino
echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega328old -p /dev/ttyUSB_NANO ./arduino
echo "> Uploaded"