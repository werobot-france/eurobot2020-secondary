const WebSocket = require('ws');
const Dualshock = require('dualshock')

const ws = new WebSocket('ws://localhost:8000');

let isWebsocketReady = false

ws.on('open', () => {
    console.log('> websocket opened')
    isWebsocketReady = true

    ws.send(JSON.stringify({ t: 'init' }))
});

ws.on('close', () => {
    isWebsocketReady = false
    console.log('> websocket disconnected');
});

function connect() {
    let devicesList = Dualshock.getDevices();
    if (isWebsocketReady && devicesList.length != 0) {

        let device = devicesList[0]
        let gamepad = Dualshock.open(device, {
            smoothAnalog: 10,
            smoothMotion: 15,
            joyDeadband: 4,
            moveDeadband: 4
        })

        //console.log('new device detected: ', device)
        
        ws.send(JSON.stringify({
            t: 'device',
            d: device
        }))

        // gamepad.onmotion = (data, d1) => {
        //     console.log(data, d1)
        // };
        // get battery status
        // gamepad.onstatus = (data, status) => {
        //     console.log(data, status)
        // };
        gamepad.ondigital = function (button, value) {
            ws.send(JSON.stringify({
                t: 'digital_input',
                d: [button, value]
            }))
        }
        gamepad.onanalog = function (axis, value) {
            ws.send(JSON.stringify({
                t: 'analog_input',
                d: [axis, value]
            }))
        }
        gamepad.ondisconnect = function () {
            connect()
            console.log(JSON.stringify({
                t: 'disconnection'
            }))
        }
        ws.on('message', (data) => {
            let body = JSON.parse(data)
            if (body.t == 'led') {
                gamepad.setLed(body.d[0], body.d[1], body.d[2])
            }
            if (body.t == 'rumble_set') {
                gamepad.rumble(body.d[0], body.d[1])
            }
            if (body.t == 'rumble_add') {
                gamepad.rumbleAdd(body.d[0], body[1], body[2], body[3])
            }
            if (body.t == 'rumble_off') {
                gamepad.rumble(0, 0)
            }
        })
        return true
    } else {
        setTimeout(connect, 1000)
    }
}
    
connect()