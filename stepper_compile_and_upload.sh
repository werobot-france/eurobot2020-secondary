echo "COMPILE AND UPLOAD SCRIPT FOR STEPPER"

cp ./arduino_commons/* ./arduino_stepper

arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328old ./arduino_stepper

rm ./arduino_stepper/SerialProtocol.cpp ./arduino_stepper/SerialProtocol.h

echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega328old -p /dev/ttyUSB0 ./arduino_stepper
echo "> Uploaded"
