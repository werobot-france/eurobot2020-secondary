const SerialPort = require('serialport')

module.exports = class ArduinoInterface {

    constructor(path, label, baudRate = 9600) {
        this.path = path
        this.label = label
        this.port = new SerialPort(this.path, {baudRate})

        this.port.on('error', (err) => {
            console.log(`ARDUINO: Serial error on port (${this.path} - ${this.label}):`, err.message)
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
                    return console.log(`ARDUINO: Write error on port (${this.path} - ${this.label}):`, err.message)
                }
                //console.log('message written')
            })
        })
    }
}