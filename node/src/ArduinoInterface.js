const SerialPort = require('serialport')

module.exports = class Arduino {

    constructor() {
        this.port = new SerialPort('/dev/ttyUSB_NANO', {baudRate: 9600})

        this.port.on('error', function(err) {
            console.log('ARDUINO: Serial port error: ', err.message)
        })
    }

    init() {
        console.log('> ARDUINO: Wait for arduino serial connexion...')
        return new Promise((resolve) => {
            // this.sendCommand('PING').then(() => {
            //     console.log('INIT DONE!')
            // })
            setTimeout(() => {
                resolve()
            }, 1000)
        })
    }

    sendCommand(name, params = []) {
        return new Promise((resolve) => {
            let toSend = name
            params.forEach(element => {
                toSend += "#" + element
            });
            //console.log(toSend)
            
            toSend += "\n"

            this.port.removeAllListeners('data')
            this.port.on('data', (data) => {
                //console.log(data.toString())
                resolve()
            })
            this.port.write(toSend, (err) => {
                if (err) {
                    return console.log('ARDUINO: Error on write: ', err.message)
                }
                //console.log('message written')
            })
        })
    }
}