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

let wait = timeout => {
  return new Promise(resolve => {
    setTimeout(resolve, timeout)
  })
}

let confirm = () => {
  return new Promise(resolve => {
    process.stdin.setEncoding('utf-8')
    console.log("Confirm ?")
    process.stdin.on('data', () => {
      resolve()
    })
  })
}

/**
 * Low hardware layer
 */
let dualshock = new (require('./src/Dualshock'))()
let pwmInterface = new (require('./src/PWMInterface'))()

let navigation = new Navigation(pwmInterface)

let container = new Container()
const main = async () => {
  // await arduinoManager.bindArduino()

  // let inventory = arduinoManager.getInstanceInventory()
  // if (inventory.length === 0) {
  //   console.error("> ERR: The stepper arduino is missing")
  //   process.exit(-1)
  // }
  // console.log("> Main: Arduino Inventory done:")
  // console.log(inventory)
  // stepperInterface = arduinoManager.getStepperArduino()

  container.set('dualshock', dualshock)

  /**
   * High hardware layer
   */
  container.set('navigation', navigation)
  //container.set('encoder', new Encoder(arduinoManager))

  /**
   * Controller
   */
  new ControlHandler(container).init()

  dualshock.on('connected', () => {
    console.log('> Main: Got controller!')
    // dualshock.rumble(150, 150, 0, 0, 0.2)
    // dualshock.setLed(0, 255, 255)
  })
  await pwmInterface.init()

  dualshock.connect()

  console.log('> Main: Init sequence done')

}

process.on('SIGINT', async () => {
  console.log("> EXIT: Caught interrupt signal")
  navigation.stop()
  pwmInterface.stop()
  setTimeout(() => {
    console.log('STOP')
    process.exit()
  }, 1000)
})

main()
