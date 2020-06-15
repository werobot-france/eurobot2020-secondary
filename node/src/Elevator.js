module.exports = class Elevator {

  constructor(params) {
    this.id = params.id
    this.label = params.label
    this.clawSlot = params.clawSlot
    this.pwmInterface = params.pwmInterface
    this.arduinoInterface = params.arduinoInterface
    this.clawOpened = false
    this.direction = 'ORIGIN' // positive
    this.enabled = true
  }

  disable() {
    this.enabled = false
  }

  enable() {
    this.enabled = true
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

  async goToMiddle() { await this.goTo(383, 800) }

  async goToTop() { await this.goTo(850, 400) }

  async goToUnStackPos() { await this.goTo(96, 800) }

  setAcceleration(value) {
    this.arduinoInterface.sendCommand('ELEVATOR_SET_ACCELERATION', [this.id, value]);
  }

  async goTo(position, speed) {
    if (!this.enabled)
      return false
    await this.arduinoInterface.sendCommand('ELEVATOR_GO_TO', [this.id, -position, speed]);
  }

  async setSpeed(speed) {
    if (!this.enabled)
      return false
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