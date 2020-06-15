module.exports = class Encoder {
  constructor(arduinoManager) {
    this.arduinoManager = arduinoManager
  }

  waitUntil(steps = 0) {
    // enable encoder with the step expected
    // block the code with a promise
    return new Promise(async resolve => {
      await this.arduinoManager.getEncoderArduino().sendCommand('ENCODER_UNTIL', [steps]) // this will reset and will send a command when finished
      resolve()
    })
  }

  navigateSteps(steps = 0, speed = 0) {

  }
}
