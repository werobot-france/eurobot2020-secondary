module.exports = class Encoder {
    constructor(arduinoManager) {
        this.arduino = arduinoManager.getEncoderArduino()
    }

    waitUntil(steps = 0) {
        // enable encoder with the step expected
        // block the code with a promise
        return new Promise(async resolve => {
            await this.arduino.sendCommand('ENCODER_WAIT', [steps]) // this will reset and will send a command when finished
            resolve()
        })
    }

    navigateSteps(steps = 0, speed = 0) {
        
    }
}
