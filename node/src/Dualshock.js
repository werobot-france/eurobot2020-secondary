const dualshock = require('dualshock')
const EventEmitter = require('events')

module.exports = class Dualshock extends EventEmitter {

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
    
            console.log('New device detected: ', device)
            
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
                
                
            }
            this.controller.ondisconnect = () => {
                console.log('> Disconnexion')
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
            setTimeout(connect, 1000)
        }
    }

}
