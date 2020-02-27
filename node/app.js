const Dualshock = require('./src/Dualshock')
let pwmInterface = new (require('./src/PWMInterface'))()
let arduinoInterface = new (require('./src/ArduinoInterface'))("/dev/ttyUSB_NANO")
let navigation = new (require('./src/Navigation'))(pwmInterface)

let drawer = new (require('./src/Drawer'))({
    pwmInterface,
    arduinoInterface
})
let leftElevator = new (require('./src/Elevator'))({
    id: 0,
    pwmInterface,
    arduinoInterface,
    clawSlot: 11
})
let rightElevator = new (require('./src/Elevator'))({
    id: 1,
    pwmInterface,
    arduinoInterface,
    clawSlot: 10
})
let screenInterface = new (require('./src/ScreenInterface'))({arduinoInterface})
let flags = new (require('./src/Flag'))({pwmInterface, servoSlot: 4})

let dualshock = new Dualshock()

const process = require('process')

dualshock.on('crossPressed', () => {
    console.log('cross pressed!')
})


let mappyt = (x, inMin, inMax, outMin, outMax) => {
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
}

let minSpeed = 0
let maxSpeed = 100

let radiusThreshold = 0.1

let currentSpeed = minSpeed

let isL2Triggered = false
let isR2Triggered = false

let leftSpeed = 0
let leftOldSpeed = 0

let rightSpeed = 0
let rightOldSpeed = 0

dualshock.on('l2Pressed', () => {
    console.log('l2 pressed!')
    isL2Triggered = true
})

dualshock.on('l2Released', () => {
    console.log('l2 released!')
    isL2Triggered = false

    leftElevator.setSpeed(0)
    leftOldSpeed = 0
    leftSpeed = 0
})

dualshock.on('l1Pressed', () => {
    leftElevator.toggleClaw()
})

/// RIGHT ELEVATOR
dualshock.on('r2Pressed', () => {
    console.log('r2 pressed!')
    isR2Triggered = true
})

dualshock.on('r2Released', () => {
    console.log('r2 released!')
    isR2Triggered = false

    rightElevator.setSpeed(0)
    rightOldSpeed = 0
    rightSpeed = 0
})

dualshock.on('r1Pressed', () => {
    rightElevator.toggleClaw()
})

// dualshock.on('upPressed', () => {
//     arduino.sendCommand('ELEVATOR_GO_TO', [0, -800, -125])
// })

dualshock.on('squarePressed', () => {
    //arduino.sendCommand('ELEVATOR_GO_TO', [0, -70, -125]) // PRESET TO CATCH BUOS

    console.log('RIGHT: Go to origin!')
    rightElevator.goToOrigin()
})

// dualshock.on('l1Pressed', () => {
//     arduino.sendCommand('ELEVATOR_GO_TO', [0, -650, -115])
// })

dualshock.on('trianglePressed', () => {
    drawer.toggle()
})

let combineSqueezer = false

dualshock.on('optionsPressed', () => {
    combineSqueezer = true
})

// dualshock.on('optionsReleased', () => {
//     combineSqueezer = false
// })

dualshock.on('circlePressed', () => {
    if (!combineSqueezer) {
        drawer.toggleSqueezer()
    }
})

dualshock.on('circleReleased', () => {
    if (combineSqueezer) {
        drawer.completlySqueeze()
        combineSqueezer = false
    }
})

dualshock.on('crossPressed', () => {
    console.log('Go to origin!')
    leftElevator.goToOrigin()
})

dualshock.on('psPressed', () => {
    console.log('EMERGENCY STOP!')
    arduinoInterface.sendCommand('STOP')
    navigation.stopAll()
})

dualshock.on('leftPressed', () => {
    console.log('Toggle direction on left')
    leftElevator.toggleDirection()
    if ((leftElevator.getDirection() == 'END' && leftSpeed > 0) || (leftElevator.getDirection() == 'ORIGIN' && leftSpeed < 0)) {
        leftSpeed = -leftSpeed
    }
    leftElevator.setSpeed(leftSpeed)
})

dualshock.on('rightPressed', () => {
    console.log('Toggle direction on right')
    rightElevator.toggleDirection()
    if ((rightElevator.getDirection() == 'END' && rightSpeed > 0) || (rightElevator.getDirection() == 'ORIGIN' && rightSpeed < 0)) {
        rightSpeed = -rightSpeed
    }
    rightElevator.setSpeed(rightSpeed)
})

dualshock.on('analog', values => {
    //console.log('analog', values)
    let lStickX = values.lStickX
    let lStickY = -values.lStickY
    let rStickX = values.rStickX
    let rStickY = -values.rStickY
    l2 = values['l2']
    r2 = values['r2']

    let leftRadius = parseFloat(Math.sqrt(Math.abs(lStickX)**2 + Math.abs(lStickY)**2)).toFixed(2)
    let rightRadius = parseFloat(Math.sqrt(Math.abs(rStickX)**2 + Math.abs(rStickY)**2)).toFixed(2)
    
    if (leftRadius > 1) {
        radius = 1
    }
    if (rightRadius > 1) {
        radius = 1
    }

    /*
    Math.abs(lStickX) <= seuil &&
    Math.abs(lStickY) <= seuil &&
    Math.abs(rStickX) <= seuil &&
    Math.abs(rStickY) <= seuil
    */
    if (rightRadius <= radiusThreshold && leftRadius <= radiusThreshold) {
        //console.log('STOP ALL')
        navigation.stopAll()
    } else {
        // if (isL2Triggered) {
        //     //currentSpeed = mappyt(l2, -1, 1, 0, 1) * 100
        //     /**
              
        //      */
        //     currentSpeed = (l2 + 1) * 50
        //     console.log(currentSpeed)
        // } else {
        //     currentSpeed = mappyt(radius, 0, 1, minSpeed, maxSpeed)
        // }

        
        if (!(rightRadius <= radiusThreshold)) {

            currentSpeed = mappyt(rightRadius, 0, 1, minSpeed, maxSpeed)

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
                console.log('south east translation')
                navigation.southEastTranslation(currentSpeed)
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
                console.log('north west translation')
                navigation.northWestTranslation(currentSpeed)
            }
        }

        if (lStickY < 0.5 * lStickX && lStickY >= -0.5 * lStickX) {

            currentSpeed = mappyt(leftRadius, 0, 1, minSpeed, maxSpeed)

            console.log('clockwise')
            navigation.clockwiseRotation(currentSpeed)
        }

        if (lStickY < -0.5 * lStickX && lStickY >= 0.5 * lStickX) {

            currentSpeed = mappyt(leftRadius, 0, 1, minSpeed, maxSpeed)

            console.log('anticlockwise')
            navigation.antiClockwiseRotation(currentSpeed)
        }
    }

    if (isL2Triggered) {
        leftSpeed = parseInt(mappyt(l2, -1, 1, 0, 400).toFixed(0))
        
        if (leftSpeed > 0 && leftSpeed < 100) {
            leftSpeed = 100
        } else if (leftSpeed >= 100 && leftSpeed < 200) {
            leftSpeed = 200
        } else if (leftSpeed >= 200 && leftSpeed < 300) {
            leftSpeed = 300
        } else if (leftSpeed >= 300 && leftSpeed <= 400) {
            leftSpeed = 400
        }
        
        if (leftElevator.getDirection() == 'END') {
            leftSpeed = -leftSpeed
        }

        if (leftSpeed != leftOldSpeed) {
            console.log(leftSpeed)
            leftElevator.setSpeed(leftSpeed)
            leftOldSpeed = leftSpeed
        }
    }


    if (isR2Triggered) {
        rightSpeed = parseInt(mappyt(r2, -1, 1, 0, 400).toFixed(0))
        
        if (rightSpeed > 0 && rightSpeed < 100) {
            rightSpeed = 100
        } else if (rightSpeed >= 100 && rightSpeed < 200) {
            rightSpeed = 200
        } else if (rightSpeed >= 200 && rightSpeed < 300) {
            rightSpeed = 300
        } else if (rightSpeed >= 300 && rightSpeed <= 400) {
            rightSpeed = 400
        }
        
        if (rightElevator.getDirection() == 'END') {
            rightSpeed = -rightSpeed
        }

        if (rightSpeed != rightOldSpeed) {
            console.log(rightSpeed)
            rightElevator.setSpeed(rightSpeed)
            rightOldSpeed = rightSpeed
        }
    }
})

let main = async () => {
    await pwmInterface.init()

    // // close squeezer
    // pwmInterface.setAngle(8, 180)

    // // close claw
    // pwmInterface.setAngle(11, 180)
    
    await navigation.stopAll()

    await arduinoInterface.init()

    screenInterface.init()
    screenInterface.print([
        "Hello, World!",
        "Go to werobot.fr"
    ])
    
    flags.close()

    // await arduino.sendCommand('ELEVATOR_GO_TO', [0, 0])

    // await arduino.sendCommand('DRAWER_GO_TO_BACK')

    //await leftElevator.setup()


    //await arduino.sendCommand('ELEVATOR_GO_TO', [0, -100, -300])
    
    dualshock.connect()

    console.log('Init sequence done')

    // TODO: Start a timer which end after 100 seconds or 1 min and 40 seconds WHEN the match start
    // flag.startTimer()
    // setTimeout(() => {
    //     console.log('END OF THE MATCH !!')
    //     arduinoInterface.sendCommand('STOP')

    // }, 100 * 1000)
}

process.on('exit', (code) => {   
    console.log('About to exit with code:', code);
    navigation.stopAll()
    arduinoInterface.sendCommand('STOP')
});
process.on('SIGINT', () => {
    console.log("Caught interrupt signal");

    process.exit();
});

main()