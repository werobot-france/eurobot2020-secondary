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

    init() {
        return new Promise((resolve, reject) => {
            this.driver = new Pca9685Driver(this.options, error => {
                if (error) {
                    console.error("Error initializing PCA9685")
                    reject()
                    process.exit(-1)
                    return
                }
                console.log("PCA9685: Initialization done")

                resolve()
            })
        })
    }
    
    mappyt(x, inMin, inMax, outMin, outMax) {
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
    }

    setAngle(slot, angle) {
        this.driver.setPulseLength(slot, this.mappyt(angle, 0, 180, 500, 1900))
    }

    /**
     * 
     * @param {int} slot 
     * @param {int} speed from -100 to 100
     */
    setEsc(slot, speed) {
        this.driver.setPulseLength(slot, ((this.mappyt(speed, 0, 100, 307, 410) / 4096) * 20) * 1000);
    }

}

