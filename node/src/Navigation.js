module.exports = class Navigation {

    constructor(pwmInterface) {
        this.escSlots = {
            frontLeft: 15,
            frontRight: 12,
            backLeft: 14,
            backRight: 13
        }
        this.pwmInterface = pwmInterface
    }
    
    setSpeed(values) {
        Object.keys(values).forEach(i => {
            this.pwmInterface.setEsc(this.escSlots[i], values[i])
        })
    }

    eastTranslation(speed) {
        this.setSpeed({
            frontLeft: speed,
            frontRight: speed,
            backLeft: speed,
            backRight: speed
        })
    }

    southTranslation(speed) {
        this.northTranslation(-speed)
    }

    northTranslation(speed) {
        this.setSpeed({
            frontLeft: speed,
            frontRight: -speed,
            backLeft: -speed,
            backRight: speed
        })
    }

    westTranslation(speed) {
        this.eastTranslation(-speed)
    }

    clockwiseRotation(speed) {
        this.setSpeed({
            frontLeft: speed,
            frontRight: speed,
            backLeft: -speed,
            backRight: -speed
        })
    }
    
    antiClockwiseRotation(speed) {
        this.clockwiseRotation(-speed)
    }

    northEastTranslation(speed) {
        this.setSpeed({
            'frontLeft': speed,
            'frontRight': 0,
            'backLeft': 0,
            'backRight': speed
        })
    }

    southWestTranslation(speed) {
        this.northEastTranslation(-speed)
    }

    northWestTranslation(speed) {
        this.setSpeed({
            'frontLeft': 0,
            'frontRight': speed,
            'backLeft': speed,
            'backRight': 0
        })
    }

    southEastTranslation(speed) {
        this.northWestTranslation(-speed)
    }

    stop() {
        this.setSpeed({
            'frontLeft': 0,
            'frontRight': 0,
            'backLeft': 0,
            'backRight': 0
        })
    }
}
