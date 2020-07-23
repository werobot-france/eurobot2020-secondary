echo "COMPILE AND UPLOAD SCRIPT FOR SWITCH"

cp ./arduino_commons/* ./arduino_switches

arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega168 ./arduino_switches

rm ./arduino_switches/SerialProtocol.cpp ./arduino_switches/SerialProtocol.h

echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega168 -p /dev/ttyUSB1 ./arduino_switches
echo "> Uploaded"
