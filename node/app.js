console.log('Initializing...')

/**
 * Imports
 */
const process = require('process')
const Navigation = require('./src/Navigation')
const Drawer = require('./src/Drawer')
const Elevator = require('./src/Elevator')
const ScreenInterface = require('./src/ScreenInterface')
const Flag = require('./src/Flag')
const Encoder = require('./src/Encoder')
const Stacker = require('./src/Stacker')
const UnStacker = require('./src/UnStacker')
const ControlHandler = require('./src/ControlHandler')
const Container = require('./src/Container')

/**
 * Low hardware layer
 */
let dualshock = new (require('./src/Dualshock'))()
let pwmInterface = new (require('./src/PWMInterface'))()
//let arduinoInterface = new (require('./src/ArduinoInterface'))("/dev/ttyUSB_NANO")
let arduinoManager = new (require('./src/ArduinoManager'))()

let stepperInterface = null
let container = new Container()
const main = async () => {
  await arduinoManager.bindArduino()

  let inventory = arduinoManager.getInstanceInventory()
  if (inventory.length === 0) {
    console.error("> ERR: The stepper arduino is missing")
    process.exit(-1)
  }
  console.log("> Main: Arduino Inventory done:")
  console.log(inventory)
  stepperInterface = arduinoManager.getStepperArduino()

  container.set('pwmInterface', pwmInterface)
  container.set('dualshock', dualshock)
  container.set('arduinoManager', arduinoManager)
  container.set('stepperInterface', stepperInterface)

  /**
   * High hardware layer
   */
  let navigation = new Navigation(pwmInterface)
  container.set('drawer', new Drawer({
    pwmInterface,
    stepperInterface
  }))
  container.set('leftElevator', new Elevator({
    id: 0,
    label: 'left',
    pwmInterface,
    stepperInterface,
    clawSlot: 11
  }))
  container.set('rightElevator', new Elevator({
    id: 1,
    label: 'right',
    pwmInterface,
    stepperInterface,
    clawSlot: 10
  }))
  container.set('screenInterface', new ScreenInterface({ stepperInterface }))
  container.set('flag', new Flag({ pwmInterface, servoSlot: 4 }))
  //container.set('encoder', new Encoder(arduinoManager))

  /**
   * Routines
   */
  container.set('stacker', new Stacker(container))
  container.set('unstacker', new UnStacker(container))

  /**
   * Controller
   */
  new ControlHandler(container).init()

  dualshock.on('connected', () => {
    console.log('> Main: Got controller!')
    dualshock.rumble(150, 150, 0, 0, 0.2)
    dualshock.setLed(0, 255, 255)
  })

  //await encoder.waitUntil(-10)


  await pwmInterface.init()

  // // close squeezer
  // pwmInterface.setAngle(8, 180)

  // // close claw
  // pwmInterface.setAngle(11, 180)

  await navigation.stop()

  //arduinoInterface.sendCommand('ACCL#100000')

  //screenInterface.init()
  /*screenInterface.print([
      "Hello, World!",
      "Go to werobot.fr"
  ])*/

  //flags.close()

  // await arduino.sendCommand('ELEVATOR_GO_TO', [0, 0])

  // await arduino.sendCommand('DRAWER_GO_TO_BACK')

  //await leftElevator.setup()


  //await arduino.sendCommand('ELEVATOR_GO_TO', [0, -100, -300])

  dualshock.connect()

  console.log('> Main: Init sequence done')

  // TODO: Start a timer which end after 100 seconds or 1 min and 40 seconds WHEN the match start
  // DO NOT ACCEPT ANY INPUT FROM THE CONTROLLER
  // flag.startTimer()
  // setTimeout(() => {
  //     console.log('END OF THE MATCH !!')
  //     arduinoInterface.sendCommand('STOP')

  // }, 100 * 1000)
}

process.on('SIGINT', () => {
  console.log("> EXIT: Caught interrupt signal")
  pwmInterface.stop()
  stepperInterface.sendCommand('STOP')
  setTimeout(() => {
    process.exit()
  }, 500)
})

main()
