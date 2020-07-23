echo "COMPILE AND UPLOAD SCRIPT FOR ENCODER"

cp ./arduino_commons/* ./arduino_encoder

arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega168 ./arduino_encoder

rm ./arduino_encoder/SerialProtocol.cpp ./arduino_encoder/SerialProtocol.h

echo "> Compiled"
arduino-cli upload --fqbn arduino:avr:nano:cpu=atmega168 -p /dev/ttyUSB0 ./arduino_encoder
echo "> Uploaded"
