const Dualshock = require('./src/Dualshock')
let pwmInterface = new (require('./src/PWMInterface'))()
let navigation = new (require('./src/Navigation'))(pwmInterface)

let arduino = new (require('./src/Arduino'))()

let dualshock = new Dualshock()
const process = require('process')

dualshock.on('crossPressed', () => {
    console.log('cross pressed!')
})


let mappyt = (x, inMin, inMax, outMin, outMax) => {
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
}

let minSpeed = 25

let currentSpeed = minSpeed

let isL2Triggered = false

let pince = false

let drawer = false

let squeezer = false

let position = 0

dualshock.on('l2Pressed', () => {
    console.log('l2 pressed!')
    isL2Triggered = true
})

dualshock.on('l2Released', () => {
    console.log('l2 pressed!')
    isL2Triggered = false
})

dualshock.on('r1Pressed', () => {
    if (!pince) {
        pwmInterface.setAngle(11, 40)
    } else {
        pwmInterface.setAngle(11, 160)
    }
    pince = !pince
})

dualshock.on('upPressed', () => {
    arduino.sendCommand('ELEVATOR_GO_TO', [0, -800, -125])
})


dualshock.on('squarePressed', () => {
    arduino.sendCommand('ELEVATOR_GO_TO', [0, -70, -125])
})

dualshock.on('l1Pressed', () => {
    arduino.sendCommand('ELEVATOR_GO_TO', [0, -650, -115])
})

dualshock.on('trianglePressed', () => {
    if (!drawer) {
        arduino.sendCommand('DRAWER_GO_TO_FRONT')
    } else {
        pwmInterface.setAngle(8, 180)
        if (squeezer) {
            setTimeout(() => {
                arduino.sendCommand('DRAWER_GO_TO_BACK')
            }, 600)
        } else {
            arduino.sendCommand('DRAWER_GO_TO_BACK')
        }
    }
    drawer = !drawer
})


dualshock.on('circlePressed', () => {
    console.log('squeezer')
    console.log(drawer)
    if (drawer) {
        if (!squeezer) {
            pwmInterface.setAngle(8, 90)
        } else {
            pwmInterface.setAngle(8, 160)
        }
        squeezer = !squeezer
    }
})

dualshock.on('crossPressed', () => {
    console.log('Go to origin!')
    arduino.sendCommand('ELEVATOR_GO_TO', [0, 0])
})

dualshock.on('analog', values => {
    console.log('analog', values)
    let seuil = 0.1
    let lStickX = values.lStickX
    let lStickY = -values.lStickY
    let rStickX = values.rStickX
    let rStickY = -values.rStickY
    l2 = values['l2']

    if (Math.abs(lStickX) <= seuil &&
        Math.abs(lStickY) <= seuil &&
        Math.abs(rStickX) <= seuil &&
        Math.abs(rStickY) <= seuil) {
        console.log('STOP ALL')
        navigation.stopAll()
    } else {
        if (isL2Triggered) {
            currentSpeed = mappyt(l2, -1, 1, 0, 1) * 100
        } else {
            currentSpeed = minSpeed
        }

        
        if (!(Math.abs(rStickX) <= seuil && Math.abs(rStickY) <= seuil)) {
            if (rStickY < 0.5 * rStickX && rStickY >= -0.5 * rStickX) {
                console.log('east translation')
                navigation.eastTranslation(currentSpeed)
            }
            if (rStickY > 0.5 * rStickX && rStickY <= 2 * rStickX) {
                console.log('north east translation')
                navigation.northEastTranslation(currentSpeed)
            }
            if (rStickY > 2 * rStickX && rStickY >= -2 * rStickX) {
                console.log('north translation')
                navigation.northTranslation(currentSpeed)
            }
            if (rStickY < -2 * rStickX && rStickY >= -0.5 * rStickX) {
                console.log('north west translation')
                navigation.northWestTranslation(currentSpeed)
            }
            if (rStickY < -0.5 * rStickX && rStickY >= 0.5 * rStickX) {
                console.log('west translation')
                navigation.westTranslation(currentSpeed)
            }
            if (rStickY < 0.5 * rStickX && rStickY >= 2 * rStickX) {
                console.log('south west translation')
                navigation.southWestTranslation(currentSpeed)
            }
            if (rStickY < 2 * rStickX && rStickY <= -2 * rStickX) {
                console.log('south translation')
                navigation.southTranslation(currentSpeed)
            }
            if (rStickY > -2 * rStickX && rStickY <= -0.5 * rStickX) {
                console.log('south east translation')
                navigation.southEastTranslation(currentSpeed)
            }
        }

        if (lStickY < 0.5 * lStickX && lStickY >= -0.5 * lStickX) {
            console.log('clockwise')
            navigation.clockwiseRotation(currentSpeed)
        }

        if (lStickY < -0.5 * lStickX && lStickY >= 0.5 * lStickX) {
            console.log('anticlockwise')
            navigation.antiClockwiseRotation(currentSpeed)
        }
    }
})

let main = async () => {
    await pwmInterface.init()

    // close squeezer
    pwmInterface.setAngle(8, 180)

    // close claw
    pwmInterface.setAngle(11, 180)
    
    await navigation.stopAll()

    await arduino.init()

    await arduino.sendCommand('ELEVATOR_GO_TO', [0, 0])

    await arduino.sendCommand('DRAWER_GO_TO_BACK')

    console.log('hello')


    //await arduino.sendCommand('ELEVATOR_GO_TO', [0, -100, -300])
    
    dualshock.connect()

    console.log('Init sequence done')
}

process.on('exit', (code) => {   
    console.log('About to exit with code:', code);
    navigation.stopAll()
});
process.on('SIGINT', () => {
    console.log("Caught interrupt signal");

    process.exit();
});

main()
