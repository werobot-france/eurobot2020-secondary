
arduinoManager =  new (require('../src/ArduinoManager'))()

let main = async () => {

    await arduinoManager.bindArduino()
    
    //console.log(arduinoManager.getStepperArduino())
    console.log('bind done')
}


main()