const fs = require('fs')
const ArduinoInterface = require('./ArduinoInterface')

module.exports = class ArduinoManager {

    constructor() {
        this.instances = []
    }

    /**
     * We will look every serial port
     * We will filter by vendor id
     * We will send each a command to known the label ('stepper' or 'encoder')
     */
    bindArduino() {
        return new Promise(async (resolve) => {
            let dir = fs.readdirSync('/dev').filter(dir => dir.indexOf('ttyUSB') > -1)
            for (var i = 0; i < dir.length; i++) {
                let arduino = new ArduinoInterface('/dev/' + dir[i])
                await arduino.init()
                console.log(`> ARDUINO: detected ${arduino.getLabel()} on port ${arduino.getPath()}`)
                this.instances.push(arduino)
            }
            resolve()
        })
    }

    /**
     * Will return the Arduino interface for the encoder arduino
     */
    getEncoderArduino() {
        return this.instances.filter(arduino => arduino.getLabel() === 'ENCODER')[0]
    }

    /**
     * Will return the Arduino interface for the stepper arduino
     */
    getStepperArduino() {
        return this.instances.filter(arduino => arduino.getLabel() === 'STEPPER')[0]
    }


}

