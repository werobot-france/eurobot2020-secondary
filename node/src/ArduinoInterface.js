const SerialPort = require('serialport')

module.exports = class ArduinoInterface {

    constructor(path) {
        this.port = new SerialPort(path, {baudRate: 9600})

        this.port.on('error', function(err) {
            console.log('Error: ', err.message)
        })
    }

    init() {
        console.log('> Wait for arduino serial connexion...')
        return new Promise((resolve, reject) => {
            // this.sendCommand('PING').then(() => {
            //     console.log('INIT DONE!')
            // })
            setTimeout(() => {
                resolve()
            }, 2000)
        })
    }

    sendCommand(name, params = []) {
        return new Promise((resolve, reject) => {
            let toSend = name
            params.forEach(element => {
                toSend += "#" + element
            });
            console.log(toSend)
            toSend += "\n"


            this.port.removeAllListeners('data')
            this.port.on('data', (data) => {
                console.log(data.toString())
                resolve()
            })
            this.port.write(toSend, (err) => {
                if (err) {
                    return console.log('Error on write: ', err.message)
                }
                console.log('message written')
            })
        })
    }
}