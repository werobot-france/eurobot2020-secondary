let Arduino = require('./arduino.js')
let arduino = new Arduino()

arduino.init().then(() => {
            arduino.isAlive().then(() => {
                console.log('GENERAL: ROBOT READY')
	    })
})
