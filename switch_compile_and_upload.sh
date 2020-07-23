echo "COMPILE AND UPLOAD SCRIPT FOR SWITCH"

cp ./arduino_commons/* ./arduino_switch

arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega168 ./arduino_switch

rm ./arduino_switch/SerialProtocol.cpp ./arduino_switch/SerialProtocol.h

echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega168 -p /dev/ttyUSB1 ./arduino_switch
echo "> Uploaded"
