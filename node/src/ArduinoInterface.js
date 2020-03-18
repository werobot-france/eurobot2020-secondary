const SerialPort = require('serialport')

module.exports = class ArduinoInterface {

    constructor(path, label = null, baudRate = 9600) {
        this.path = path
        this.label = label

        this.port = new SerialPort(this.path, {baudRate})

        this.port.on('error', (err) => {
            console.log(`ARDUINO: Serial error on port (${this.path} - ${this.label}):`, err.message)
        })
    }

    setLabel(label) {
        this.label = label
    }

    getLabel() {
        return this.label
    }

    getPath() {
        return this.path
    }

    wait(time) { return new Promise(resolve => setTimeout(resolve, time * 1000)) }

    init() {
        return new Promise(async (resolve) => {
            //await this.sendCommand("PING", [], false)
            
            await this.wait(1.5)

            let response = await this.sendCommand("ID")
            
            if (response.substr(0, 3) !== 'ID:') {
                console.log(`ERR: Arduino Interface (${this.path} - ${this.label}) failed to initialize`)
                console.log("EST-CE QUE TU CROIT QUE C'EST DU RESPECT ça MON GARçON ?")
                return;
            }

            let toIdentify = ['ENCODER', 'STEPPER']
            toIdentify.forEach(label => {
                if (response.substr(3) === label) {
                    this.setLabel(label)
                }
            })

            resolve()
        })
    }

    sendCommand(name, params = [], expectResponse = true) {
        return new Promise((resolve) => {
            let toSend = name
            params.forEach(element => {
                toSend += "#" + element
            });
            //console.log(toSend)
            console.log(' --> ' + toSend)
            
            toSend += "\n"

            this.port.removeAllListeners('data')
            if (expectResponse) {
                this.port.on('data', (data) => {
                    data = data.toString().replace('\n', '')
                    data = data.substr(0, data.length - 1)
                    console.log(' --< ' + data)
                    resolve(data)
                })
            }
            this.port.write(toSend, (err) => {
                if (err) {
                    return console.log(`ARDUINO: Write error on port (${this.path} - ${this.label}):`, err.message)
                }
                if (!expectResponse) {
                    resolve()
                }
                //console.log('message written')
            })
        })
    }

    listenAll() {
        this.port.removeAllListeners('data')
        this.port.on('data', (data) => {
            data = data.toString().replace('\n', '')
            data = data.substr(0, data.length - 1)
            console.log(' --< ' + data)
        })
    }
}