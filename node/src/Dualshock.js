const dualshock = require('dualshock')
const EventEmitter = require('events')

module.exports = class Dualshock extends EventEmitter {

  constructor() {
    super()
    this.analogValues = {
      lStickX: 0,
      lStickY: 0,
      rStickX: 0,
      rStickY: 0,
      l2: 0
    }
  }

  connect() {
    let devicesList = dualshock.getDevices();
    if (devicesList.length != 0) {

      let device = devicesList[0]
      this.controller = dualshock.open(device, {
        smoothAnalog: 10,
        smoothMotion: 15,
        joyDeadband: 4,
        moveDeadband: 4
      })

      console.log('> DUALSHOCK: Device detected: ', device)

      this.emit('connected')

      this.controller.ondigital = (button, value) => {
        let ignored = ['a', 'b', 'x', 'y']
        if (ignored.indexOf(button) !== -1)
          return
        if (button === 'start')
          button = 'options'
        if (button === 'select')
          button = 'share'
        //console.log(button, value)
        if (value)
          this.emit(button + 'Pressed')
        else
          this.emit(button + 'Released')
      }
      this.controller.onanalog = (axis, value) => {
        if (axis === 't1X' || axis === 't1Y')
          return

        value = ((value * 2 / 255) - 1).toFixed(2)

        this.analogValues[axis] = parseFloat(value)

        this.emit('analog', this.analogValues)
      }
      this.controller.ondisconnect = () => {
        console.log('> DUALSHOCK: Device disconnected')
        this.connect()
      }
      // gamepad.onmotion = (data, d1) => {
      //     console.log(data, d1)
      // };
      // get battery status
      // gamepad.onstatus = (data, status) => {
      //     console.log(data, status)
      // };

      return true
    } else {
      setTimeout(() => {
        this.connect()
      }, 1000)
    }
  }

  setLed(red = 0, green = 0, blue = 0) {
    //this.controller.setLed(red, green, blue)
  }

  rumble(left, right, durL, durR, timeout) {
    //this.controller.rumble(left, right, durL, durR)
    return new Promise(resolve => {
      setTimeout(() => {
        //this.controller.rumble(0, 0)
        resolve()
      }, timeout * 1000)
    })
  }
}
