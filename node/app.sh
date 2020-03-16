echo "Starting main app..."
# disable DTR for both serial port
stty -F /dev/ttyUSB0 -hupcl
stty -F /dev/ttyUSB1 -hupcl
node node/test/arduino.js