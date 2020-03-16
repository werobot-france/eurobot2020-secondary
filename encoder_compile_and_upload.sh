echo "COMPILE AND UPLOAD SCRIPT FOR ENCODER"
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328 ./arduino_encoder
echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega328 -p /dev/ttyUSB0 ./arduino_encoder
echo "> Uploaded"
