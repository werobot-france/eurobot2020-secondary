echo "Starting main app..."
stty -F /dev/ttyUSB0 -hupcl
stty -F /dev/ttyUSB1 -hupcl
node node/test/arduino.js