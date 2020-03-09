module.exports = class Elevator {

    constructor(params) {
        this.id = params.id
        this.label = params.label
        this.clawSlot = params.clawSlot
        this.pwmInterface = params.pwmInterface
        this.arduinoInterface = params.arduinoInterface
        this.clawOpened = false
        this.direction = 'ORIGIN' // positive
    }

    getLabel() {
        return this.label
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

    closeClawGround() {
        this.pwmInterface.setAngle(this.clawSlot, 50)
        this.clawOpened = false
        console.log('CLAW MAX CLOSED')
    }

    toggleClaw() {
        if (this.clawOpened) {
            this.closeClaw()
        } else {
            this.openClaw()
        }
    }

    async goToMiddle() {
        await this.arduinoInterface.sendCommand('ELEVATOR_GO_TO', [this.id, -383, 800]);
    }

    async goToTop() {
        await this.arduinoInterface.sendCommand('ELEVATOR_GO_TO', [this.id, -850, 400]);
    }

    async goToUnStackPos() {
        await this.arduinoInterface.sendCommand('ELEVATOR_GO_TO', [this.id, -96, 800]);

    }

    async setSpeed(speed) {
        this.arduinoInterface.sendCommand('ELEVATOR_SET_SPEED', [this.id, speed])
    }

    async getDirection() {
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
        await this.arduinoInterface.sendCommand('ELEVATOR_SET_SPEED', [this.id, 800])
    }

    async setup() {
        this.goToOrigin()
        this.closeClaw()
    }
}