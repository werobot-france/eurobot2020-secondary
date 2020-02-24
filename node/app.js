const Dualshock = require('./src/Dualshock')

let dualshock = new Dualshock()

dualshock.on('crossPressed', () => {
    console.log('cross pressed!')
})


dualshock.connect()
