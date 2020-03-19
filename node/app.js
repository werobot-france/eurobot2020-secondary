console.log('Initializing...')

/**
 * Low hardware layer
 */
let dualshock = new (require('./src/Dualshock'))()
let pwmInterface = new (require('./src/PWMInterface'))()
//let arduinoInterface = new (require('./src/ArduinoInterface'))("/dev/ttyUSB_NANO")

let arduinoManager = new (require('./src/ArduinoManager'))()

let arduinoInterface = arduinoManager.getStepperArduino()

/**
 * High hardware layer
 */
let navigation = new (require('./src/Navigation'))(pwmInterface)
let drawer = new (require('./src/Drawer'))({
    pwmInterface,
    arduinoInterface
})
let leftElevator = new (require('./src/Elevator'))({
    id: 0,
    label: 'left',
    pwmInterface,
    arduinoInterface,
    clawSlot: 11
})
let rightElevator = new (require('./src/Elevator'))({
    id: 1,
    label: 'right',
    pwmInterface,
    arduinoInterface,
    clawSlot: 10
})
let screenInterface = new (require('./src/ScreenInterface'))({arduinoInterface})
let flags = new (require('./src/Flag'))({pwmInterface, servoSlot: 4})
let encoder = new (require('./src/Encoder'))(arduinoManager)

/**
 * Routines
 */
let stacker = new (require('./src/Stacker'))({leftElevator, rightElevator, navigation})
let unStacker = new (require('./src/UnStacker'))({leftElevator, rightElevator, navigation, drawer})

const process = require('process')

dualshock.on('connected', () => {
    console.log('> MAIN: Controller connected!')
    dualshock.rumble(150, 150, 0, 0, 0.2)
    dualshock.setLed(0, 255, 255)
})

dualshock.on('crossPressed', () => {
    console.log('cross pressed!')
})

let mappyt = (x, inMin, inMax, outMin, outMax) => {
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
}

let minSpeed = 0
let maxSpeed = 40

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
    pwmInterface.stop()
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
        navigation.stop()
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

            /**
             * Linear map mappy(0, 0.9, 0, a*1000)
             * Linear map mappy(0.9, 1, a*1000, 1)
             */
            if (rightRadius <= 0.9) {
                currentSpeed = mappyt(rightRadius, 0, 0.9, minSpeed, maxSpeed)
            } else {
                currentSpeed = mappyt(rightRadius, 0.9, 1, maxSpeed, 100)
            }

            if (rStickY < 0.5 * rStickX && rStickY >= -0.5 * rStickX) {
                //console.log('east translation')
                navigation.eastTranslation(currentSpeed)
            }
            if (rStickY > 0.5 * rStickX && rStickY <= 2 * rStickX) {
                //console.log('north east translation')
                navigation.northEastTranslation(currentSpeed)
            }
            if (rStickY > 2 * rStickX && rStickY >= -2 * rStickX) {
                //console.log('north translation')
                navigation.northTranslation(currentSpeed)
            }
            if (rStickY < -2 * rStickX && rStickY >= -0.5 * rStickX) {
                //console.log('south east translation')
                navigation.southEastTranslation(currentSpeed)
            }
            if (rStickY < -0.5 * rStickX && rStickY >= 0.5 * rStickX) {
                //console.log('west translation')
                navigation.westTranslation(currentSpeed)
            }
            if (rStickY < 0.5 * rStickX && rStickY >= 2 * rStickX) {
                //console.log('south west translation')
                navigation.southWestTranslation(currentSpeed)
            }
            if (rStickY < 2 * rStickX && rStickY <= -2 * rStickX) {
                //console.log('south translation')
                navigation.southTranslation(currentSpeed)
            }
            if (rStickY > -2 * rStickX && rStickY <= -0.5 * rStickX) {
                //console.log('north west translation')
                navigation.northWestTranslation(currentSpeed)
            }
        }

        if (lStickY < 0.5 * lStickX && lStickY >= -0.5 * lStickX) {

            currentSpeed = mappyt(leftRadius, 0, 1, minSpeed, maxSpeed)

            //console.log('clockwise')
            navigation.clockwiseRotation(currentSpeed)
        }

        if (lStickY < -0.5 * lStickX && lStickY >= 0.5 * lStickX) {

            currentSpeed = mappyt(leftRadius, 0, 1, minSpeed, maxSpeed)

            //console.log('anticlockwise')
            navigation.antiClockwiseRotation(currentSpeed)
        }
    }

    if (isL2Triggered) {
        leftSpeed = parseInt(mappyt(l2, -1, 1, 0, 400).toFixed(0))
        
        if (leftSpeed > 0 && leftSpeed < 100) {
            leftSpeed = 100
        } else if (leftSpeed >= 100 && leftSpeed < 200) {
            leftSpeed = 250
        } else if (leftSpeed >= 200 && leftSpeed < 300) {
            leftSpeed = 500
        } else if (leftSpeed >= 300 && leftSpeed <= 400) {
            leftSpeed = 750
        }
        
        if (leftElevator.getDirection() == 'END') {
            leftSpeed = -leftSpeed
        }

        if (leftSpeed != leftOldSpeed) {
            //console.log(leftSpeed)
            leftElevator.setSpeed(leftSpeed)
            leftOldSpeed = leftSpeed
        }
    }

    if (isR2Triggered) {
        rightSpeed = parseInt(mappyt(r2, -1, 1, 0, 400).toFixed(0))
        
        if (rightSpeed > 0 && rightSpeed < 100) {
            rightSpeed = 100
        } else if (rightSpeed >= 100 && rightSpeed < 200) {
            rightSpeed = 250
        } else if (rightSpeed >= 200 && rightSpeed < 300) {
            rightSpeed = 500
        } else if (rightSpeed >= 300 && rightSpeed <= 400) {
            rightSpeed = 750
        }
        
        if (rightElevator.getDirection() == 'END') {
            rightSpeed = -rightSpeed
        }

        if (rightSpeed != rightOldSpeed) {
            //  console.log(rightSpeed)
            rightElevator.setSpeed(rightSpeed)
            rightOldSpeed = rightSpeed
        }
    }
})

dualshock.on('upPressed', () => {
    arduinoInterface.sendCommand('ELEVATOR_GO_TO#0#-860#800');
})
dualshock.on('downPressed', () => {
    arduinoInterface.sendCommand('ELEVATOR_GO_TO#0#-383#800');
})

// dualshock.on('l3Pressed', () => {
//     leftElevator.closeClawGround()
// })
// dualshock.on('r3Pressed', () => {
//     rightElevator.closeClawGround()
// })
dualshock.on('padPressed', () => {
    stacker.stackRoutine(['G', 'G', 'R', 'R', 'R'])
    //unStacker.unStackRoutine()
})


function wait(timeout) {
    return new Promise(resolve => {
        setTimeout(resolve, timeout)
    })
}

function confirm() {
    return new Promise(resolve => {
        process.stdin.setEncoding('utf-8');
        console.log("Confirm ?");
        process.stdin.on('data', () => {
            resolve()
        });
    })
}

dualshock.on('sharePressed', async () => {
    //arduinoInterface.sendCommand('GET_CURRENT_POSITION');
    await leftElevator.goToTop()
    console.log('go to top DONE')
    
    return
    // manual initialization
    // leftElevator.closeClaw()

    // leftElevator.goToOrigin()
    // console.log('MANUAL INITIALIZATION DONE')

    // return

    /*
    routine prendr Verre
    elevator.goToMiddle()
    elevator.openClaw()
    navigation.eastTranslation()
    elevator.goToOrigin()
    navigation.westTranslation()
    elevator.closeClaw()
    elevator.goToTop()
    */
    /*
    routine attrapage
    situation n°3 Yellow team
    GGRRR

    leftElevator.goToTop()
    // deplacement callage vers au dessus du vers
    navigation.westTranslation()
    await
    this.takeBuos(leftElevator)
    // decallage d'une boue
    navigation.westTranslation()
    await 
    this.takeBuos(leftElevator)
    // decallage d'une boue
    navigation.westTranslation()
    await 
    this.takeBuos(leftElevator)
    navigation.westTranslation()
    // decallage de deux bouées
    await
    this.takeBuos(rightElevator)
    // decallage d'une boue
    navigation.westTranslation()
    await 
    this.takeBuos(rightElevator)
    */

    await wait(1000)
    leftElevator.goToTop()
    await wait(1 * 1000)
    await confirm()
    navigation.westTranslation(50)
    await wait(0.82 * 1000)
    navigation.stop()
    leftElevator.goToMiddle()
    await wait(1000)
    leftElevator.openClaw()
    await wait(700)
    navigation.northTranslation(30)
    await wait(400)
    navigation.stop()
    await confirm()
    navigation.eastTranslation(30)
    await wait(0.45 * 1000)
    navigation.stop()
    leftElevator.goToOrigin()
    await wait(0.8 * 1000)
    await confirm()
    navigation.westTranslation(30)
    await wait(0.45 * 1000)
    navigation.stop()
    leftElevator.closeClaw()
    await wait(0.8 * 1000)
    leftElevator.goToTop()
    await wait(0.5 * 1000)
    await confirm()
    navigation.westTranslation(30)
    await wait(0.40 * 1000)
    navigation.stop()
    await confirm()
    leftElevator.goToMiddle()
    await wait(0.40 * 1000)
    leftElevator.openClaw()
    await confirm()
    navigation.eastTranslation(30)
    await wait(0.45 * 1000)
    navigation.stop()
    leftElevator.goToOrigin()
    await wait(0.8 * 1000)
    await confirm()
    navigation.westTranslation(30)
    await wait(0.45 * 1000)
    navigation.stop()
    leftElevator.closeClaw()
    await wait(0.8 * 1000)
    leftElevator.goToTop()
    await wait(0.5 * 1000)
    await confirm()
    navigation.westTranslation(30)
    await wait(0.40 * 1000)
    navigation.stop()
    await confirm()
    leftElevator.goToMiddle()
    await wait(0.40 * 1000)
    leftElevator.openClaw()
    await confirm()
    navigation.eastTranslation(30)
    await wait(0.45 * 1000)
    navigation.stop()
    leftElevator.goToOrigin()
    await wait(0.8 * 1000)
    await confirm()
    navigation.westTranslation(30)
    await wait(0.45 * 1000)
    navigation.stop()
    leftElevator.closeClaw()
    await wait(0.8 * 1000)
    leftElevator.goToTop()
})


let main = async () => {
    await arduinoManager.bindArduino()

    console.log(arduinoManager.getEncoderArduino().sendCommand)

    await encoder.waitUntil(-10)
    

    await pwmInterface.init()

    // // close squeezer
    // pwmInterface.setAngle(8, 180)

    // // close claw
    // pwmInterface.setAngle(11, 180)
    
    await navigation.stop()




    //arduinoInterface.sendCommand('ACCL#100000');

    //screenInterface.init()
    /*screenInterface.print([
        "Hello, World!",
        "Go to werobot.fr"
    ])*/
    
    //flags.close()

    // await arduino.sendCommand('ELEVATOR_GO_TO', [0, 0])

    // await arduino.sendCommand('DRAWER_GO_TO_BACK')

    //await leftElevator.setup()


    //await arduino.sendCommand('ELEVATOR_GO_TO', [0, -100, -300])
    
    dualshock.connect()

    console.log('Init sequence done')

    // TODO: Start a timer which end after 100 seconds or 1 min and 40 seconds WHEN the match start
    // DO NOT ACCEPT ANY INPUT FROM THE CONTROLLER
    // flag.startTimer()
    // setTimeout(() => {
    //     console.log('END OF THE MATCH !!')
    //     arduinoInterface.sendCommand('STOP')

    // }, 100 * 1000)
}

process.on('SIGINT', () => {
    console.log("> EXIT: Caught interrupt signal");
    pwmInterface.stop()
    arduinoInterface.sendCommand('STOP')
    setTimeout(() => {
        process.exit();
    }, 500)
});

main()
