
arduinoManager =  new (require('../src/ArduinoManager'))()

let main = async () => {

    await arduinoManager.bindArduino()
    
    //console.log(arduinoManager.getStepperArduino())
}


main()