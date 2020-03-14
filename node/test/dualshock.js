const Dualshock = require('dualshock')

function connect() {
    let devicesList = Dualshock.getDevices();
    if (devicesList.length != 0) {

        let device = devicesList[0]
        let gamepad = Dualshock.open(device, {
            smoothAnalog: 10,
            smoothMotion: 15,
            joyDeadband: 4,
            moveDeadband: 4
        })
        console.log(device)

        gamepad.ondigital = function (button, value) {
            console.log(button, value)
            if (button === 'cross' && value) {
                console.log("cross!")
                gamepad.setLed(0, 255, 0)
            }
        }
        gamepad.onanalog = function (axis, value) {
            console.log(axis, value)
        }
        gamepad.ondisconnect = function () {
            console.log("disconnexion")
        }
        //gamepad.rumbleAdd(body.d[0], body[1], body[2], body[3])
        //gamepad.rumble(0, 0)
        //gamepad.setLed(body.d[0], body.d[1], body.d[2])
        return true
    } else {
        setTimeout(connect, 1000)
    }
}
    
connect()
