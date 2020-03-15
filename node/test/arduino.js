
arduinoManager =  new (require('../src/ArduinoManager'))()

arduinoManager.init()

console.log(arduinoManager.getEncoderArduino())