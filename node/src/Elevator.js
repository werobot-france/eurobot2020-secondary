module.exports = class Elevator {

    constructor(params) {
        this.id = params.id
        this.clawSlot = params.clawSlot
        this.pwmInterface = params.pwmInterface
        this.arduinoInterface = params.arduinoInterface
        this.clawOpened = false
        this.direction = 'ORIGIN' // positive
    }

    openClaw() {
        this.pwmInterface.setAngle(this.clawSlot, 180)
        this.clawOpened = true
        console.log('CLAW OPENED')
    }

    closeClaw() {
        this.pwmInterface.setAngle(this.clawSlot, 70)
        this.clawOpened = false
        console.log('CLAW CLOSED')
    }

    toggleClaw() {
        if (this.clawOpened) {
            this.closeClaw()
        } else {
            this.openClaw()
        }
    }

    setSpeed(speed) {
        this.arduinoInterface.sendCommand('ELEVATOR_SET_SPEED', [this.id, speed])
    }

    getDirection() {
        return this.direction
    }

    toggleDirection() {
        if (this.direction === 'ORIGIN') {
            this.direction = 'END'
        } else {
            this.direction = 'ORIGIN'
        }
    }

    async goToOrigin() {
        await this.arduinoInterface.sendCommand('ELEVATOR_SET_SPEED', [this.id, 400])
    }

    async setup() {
        this.goToOrigin()
        this.closeClaw()
    }
}