const i2cBus = require("i2c-bus")
const Pca9685Driver = require("pca9685").Pca9685Driver

module.exports = class PwmInterface {

  constructor() {
    this.options = {
      i2c: i2cBus.openSync(1),
      address: 0x40,
      frequency: 50,
      debug: false
    };
  }

  /**
   * Will initialize the pwm interface
   */
  init() {
    return new Promise((resolve, reject) => {
      this.driver = new Pca9685Driver(this.options, error => {
        if (error) {
          console.error("PCA9685: Error initializing")
          reject()
          process.exit(-1)
          return
        }
        console.log("PCA9685: Initialization done")

        resolve()
      })
    })
  }

  /**
   * Simple helper function to do Cross-multiplication
   * 
   * @param {Number} x 
   * @param {Number} inMin 
   * @param {Number} inMax 
   * @param {Number} outMin 
   * @param {Number} outMax 
   */
  mappyt(x, inMin, inMax, outMin, outMax) {
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
  }

  /**
   * Control the angle of the typical servo motor
   * 
   * @param {Number} slot 
   * @param {Number} angle 
   */
  setAngle(slot, angle) {
    this.driver.setPulseLength(slot, this.mappyt(angle, 0, 180, 500, 1900))
  }

  /**
   * Set a speed for a ESC slot
   * 
   * @param {Number} slot 
   * @param {Number} speed from -100 to 100
   */
  setEsc(slot, speed) {
    this.driver.setPulseLength(slot, ((this.mappyt(speed, 0, 100, 307, 410) / 4096) * 20) * 1000);
  }

  /**
   * Turn all channels off
   */
  stop() {
    for (var i = 0; i < 15; i++) {
      this.driver.channelOff(i)
    }
  }

}

