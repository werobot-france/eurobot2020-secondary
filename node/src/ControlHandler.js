module.exports = class ControlHandler {

  constructor(container) {
    this.navigation = container.get('navigation')
    this.dualshock = container.get('dualshock')
    this.leftElevator = container.get('leftElevator')
    this.rightElevator = container.get('rightElevator')
    this.drawer = container.get('drawer')
    this.pwmInterface = container.get('pwmInterface')
    this.stepperInterface = container.get('stepperInterface')
    console.log(this.navigation)
  }

  wait(timeout) {
    return new Promise(resolve => {
      setTimeout(resolve, timeout)
    })
  }

  confirm() {
    return new Promise(resolve => {
      process.stdin.setEncoding('utf-8')
      console.log("Confirm ?")
      process.stdin.on('data', () => {
        resolve()
      })
    })
  }

  mappyt(x, inMin, inMax, outMin, outMax) {
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
  }

  init() {
    this.dualshock.on('crossPressed', () => {
      console.log('cross pressed!')
    })
    
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
  
    // this.dualshock.on('l2Pressed', () => {
    //   console.log('l2 pressed!')
    //   isL2Triggered = true
    // })
  
    // this.dualshock.on('l2Released', () => {
    //   console.log('l2 released!')
    //   isL2Triggered = false
  
    //   this.leftElevator.setSpeed(0)
    //   leftOldSpeed = 0
    //   leftSpeed = 0
    // })
  
    // this.dualshock.on('l1Pressed', () => {
    //   this.leftElevator.toggleClaw()
    // })
  
    // /// RIGHT ELEVATOR
    // this.dualshock.on('r2Pressed', () => {
    //   console.log('r2 pressed!')
    //   isR2Triggered = true
    // })
  
    // this.dualshock.on('r2Released', () => {
    //   console.log('r2 released!')
    //   isR2Triggered = false
  
    //   this.rightElevator.setSpeed(0)
    //   rightOldSpeed = 0
    //   rightSpeed = 0
    // })
  
    // this.dualshock.on('r1Pressed', () => {
    //   this.rightElevator.toggleClaw()
    // })
  
    // this.dualshock.on('upPressed', () => {
    //     arduino.sendCommand('ELEVATOR_GO_TO', [0, -800, -125])
    // })
  
    // this.dualshock.on('squarePressed', () => {
    //   //arduino.sendCommand('ELEVATOR_GO_TO', [0, -70, -125]) // PRESET TO CATCH BUOS
  
    //   console.log('RIGHT: Go to origin!')
    //   this.rightElevator.goToOrigin()
    // })
  
    // this.dualshock.on('l1Pressed', () => {
    //     arduino.sendCommand('ELEVATOR_GO_TO', [0, -650, -115])
    // })
  
    // this.dualshock.on('trianglePressed', () => {
    //   this.drawer.toggle()
    // })
  
    // let combineSqueezer = false
  
    // this.dualshock.on('optionsPressed', () => {
    //   combineSqueezer = true
    // })
  
    // // this.dualshock.on('optionsReleased', () => {
    // //     combineSqueezer = false
    // // })
  
    // this.dualshock.on('circlePressed', () => {
    //   if (!combineSqueezer) {
    //     this.drawer.toggleSqueezer()
    //   }
    // })
  
    // this.dualshock.on('circleReleased', () => {
    //   if (combineSqueezer) {
    //     this.drawer.completlySqueeze()
    //     combineSqueezer = false
    //   }
    // })
  
    // this.dualshock.on('crossPressed', () => {
    //   console.log('Go to origin!')
    //   this.leftElevator.goToOrigin()
    // })
  
    this.dualshock.on('psPressed', () => {
      console.log('EMERGENCY STOP!')
    //   this.stepperInterface.sendCommand('STOP')
      this.pwmInterface.stop()
    })
  
    // this.dualshock.on('leftPressed', () => {
    //   console.log('Toggle direction on left')
    //   this.leftElevator.toggleDirection()
    //   if (
    //     (this.leftElevator.getDirection() == 'END' && leftSpeed > 0) ||
    //     (this.leftElevator.getDirection() == 'ORIGIN' && leftSpeed < 0)
    //   ) {
    //     leftSpeed = -leftSpeed
    //   }
    //   this.leftElevator.setSpeed(leftSpeed)
    // })
  
    // this.dualshock.on('rightPressed', () => {
    //   console.log('Toggle direction on right')
    //   this.rightElevator.toggleDirection()
    //   if (
    //     (this.rightElevator.getDirection() == 'END' && rightSpeed > 0) ||
    //     (this.rightElevator.getDirection() == 'ORIGIN' && rightSpeed < 0)
    //   ) {
    //     rightSpeed = -rightSpeed
    //   }
    //   this.rightElevator.setSpeed(rightSpeed)
    // })
  
    this.dualshock.on('analog', values => {
      console.log('analog', values)
      let lStickX = values.lStickX
      let lStickY = -values.lStickY
      let rStickX = values.rStickX
      let rStickY = -values.rStickY
      let l2 = values['l2']
      let r2 = values['r2']
  
      let leftRadius = parseFloat(Math.sqrt(Math.abs(lStickX) ** 2 + Math.abs(lStickY) ** 2)).toFixed(2)
      let rightRadius = parseFloat(Math.sqrt(Math.abs(rStickX) ** 2 + Math.abs(rStickY) ** 2)).toFixed(2)
  
      let radius = 0;
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
        console.log('STOP ALL')
        this.navigation.stop()
      } else {
        // if (isL2Triggered) {
        //     //currentSpeed = this.mappyt(l2, -1, 1, 0, 1) * 100
        //     /**
  
        //      */
        //     currentSpeed = (l2 + 1) * 50
        //     console.log(currentSpeed)
        // } else {
        //     currentSpeed = this.mappyt(radius, 0, 1, minSpeed, maxSpeed)
        // }
  
  
        if (!(rightRadius <= radiusThreshold)) {
  
          /**
           * Linear map mappy(0, 0.9, 0, a*1000)
           * Linear map mappy(0.9, 1, a*1000, 1)
           */
          if (rightRadius <= 0.9) {
            currentSpeed = this.mappyt(rightRadius, 0, 0.9, minSpeed, maxSpeed)
          } else {
            currentSpeed = this.mappyt(rightRadius, 0.9, 1, maxSpeed, 100)
          }
  
          if (rStickY < 0.5 * rStickX && rStickY >= -0.5 * rStickX) {
            //console.log('east translation')
            this.navigation.eastTranslation(currentSpeed)
          }
          if (rStickY > 0.5 * rStickX && rStickY <= 2 * rStickX) {
            //console.log('north east translation')
            this.navigation.northEastTranslation(currentSpeed)
          }
          if (rStickY > 2 * rStickX && rStickY >= -2 * rStickX) {
            //console.log('north translation')
            this.navigation.northTranslation(currentSpeed)
          }
          if (rStickY < -2 * rStickX && rStickY >= -0.5 * rStickX) {
            //console.log('south east translation')
            this.navigation.southEastTranslation(currentSpeed)
          }
          if (rStickY < -0.5 * rStickX && rStickY >= 0.5 * rStickX) {
            //console.log('west translation')
            this.navigation.westTranslation(currentSpeed)
          }
          if (rStickY < 0.5 * rStickX && rStickY >= 2 * rStickX) {
            //console.log('south west translation')
            this.navigation.southWestTranslation(currentSpeed)
          }
          if (rStickY < 2 * rStickX && rStickY <= -2 * rStickX) {
            //console.log('south translation')
            this.navigation.southTranslation(currentSpeed)
          }
          if (rStickY > -2 * rStickX && rStickY <= -0.5 * rStickX) {
            //console.log('north west translation')
            this.navigation.northWestTranslation(currentSpeed)
          }
        }
  
        if (lStickY < 0.5 * lStickX && lStickY >= -0.5 * lStickX) {
  
          currentSpeed = this.mappyt(leftRadius, 0, 1, minSpeed, maxSpeed)
  
          //console.log('clockwise')
          this.navigation.clockwiseRotation(currentSpeed)
        }
  
        if (lStickY < -0.5 * lStickX && lStickY >= 0.5 * lStickX) {
  
          currentSpeed = this.mappyt(leftRadius, 0, 1, minSpeed, maxSpeed)
  
          //console.log('anticlockwise')
          this.navigation.antiClockwiseRotation(currentSpeed)
        }
      }
  
    //   if (isL2Triggered) {
    //     leftSpeed = parseInt(this.mappyt(l2, -1, 1, 0, 400).toFixed(0))
  
    //     if (leftSpeed > 0 && leftSpeed < 100) {
    //       leftSpeed = 100
    //     } else if (leftSpeed >= 100 && leftSpeed < 200) {
    //       leftSpeed = 250
    //     } else if (leftSpeed >= 200 && leftSpeed < 300) {
    //       leftSpeed = 500
    //     } else if (leftSpeed >= 300 && leftSpeed <= 400) {
    //       leftSpeed = 750
    //     }
  
    //     if (leftElevator.getDirection() == 'END') {
    //       leftSpeed = -leftSpeed
    //     }
  
    //     if (leftSpeed != leftOldSpeed) {
    //       //console.log(leftSpeed)
    //       this.leftElevator.setSpeed(leftSpeed)
    //       leftOldSpeed = leftSpeed
    //     }
    //   }
  
    //   if (isR2Triggered) {
    //     rightSpeed = parseInt(this.mappyt(r2, -1, 1, 0, 400).toFixed(0))
  
    //     if (rightSpeed > 0 && rightSpeed < 100) {
    //       rightSpeed = 100
    //     } else if (rightSpeed >= 100 && rightSpeed < 200) {
    //       rightSpeed = 250
    //     } else if (rightSpeed >= 200 && rightSpeed < 300) {
    //       rightSpeed = 500
    //     } else if (rightSpeed >= 300 && rightSpeed <= 400) {
    //       rightSpeed = 750
    //     }
  
    //     if (rightElevator.getDirection() == 'END') {
    //       rightSpeed = -rightSpeed
    //     }
  
    //     if (rightSpeed != rightOldSpeed) {
    //       //  console.log(rightSpeed)
    //       this.rightElevator.setSpeed(rightSpeed)
    //       rightOldSpeed = rightSpeed
    //     }
    //   }
    })
  
    // this.dualshock.on('upPressed', () => {
    //   arduinoInterface.sendCommand('ELEVATOR_GO_TO#0#-860#800');
    // })
    // this.dualshock.on('downPressed', () => {
    //   arduinoInterface.sendCommand('ELEVATOR_GO_TO#0#-383#800');
    // })
  
    // this.dualshock.on('l3Pressed', () => {
    //     this.leftElevator.closeClawGround()
    // })
    // this.dualshock.on('r3Pressed', () => {
    //     this.rightElevator.closeClawGround()
    // })
    // this.dualshock.on('padPressed', () => {
    //   stacker.stackRoutine(['G', 'G', 'R', 'R', 'R'])
    //   //unStacker.unStackRoutine()
    // })
  
    this.dualshock.on('sharePressed', async () => {
      //arduinoInterface.sendCommand('GET_CURRENT_POSITION');
      await this.leftElevator.goToTop()
      console.log('go to top DONE')
  
      return
      // manual initialization
      // this.leftElevator.closeClaw()
  
      // this.leftElevator.goToOrigin()
      // console.log('MANUAL INITIALIZATION DONE')
  
      // return
  
      /*
      routine prendr Verre
      elevator.goToMiddle()
      elevator.openClaw()
      this.navigation.eastTranslation()
      elevator.goToOrigin()
      this.navigation.westTranslation()
      elevator.closeClaw()
      elevator.goToTop()
      */
      /*
      routine attrapage
      situation n°3 Yellow team
      GGRRR
  
      this.leftElevator.goToTop()
      // deplacement callage vers au dessus du vers
      this.navigation.westTranslation()
      await
      this.takeBuos(leftElevator)
      // decallage d'une boue
      this.navigation.westTranslation()
      await 
      this.takeBuos(leftElevator)
      // decallage d'une boue
      this.navigation.westTranslation()
      await 
      this.takeBuos(leftElevator)
      this.navigation.westTranslation()
      // decallage de deux bouées
      await
      this.takeBuos(rightElevator)
      // decallage d'une boue
      this.navigation.westTranslation()
      await 
      this.takeBuos(rightElevator)
      */
  
      await wait(1000)
      this.leftElevator.goToTop()
      await wait(1 * 1000)
      await confirm()
      this.navigation.westTranslation(50)
      await wait(0.82 * 1000)
      this.navigation.stop()
      this.leftElevator.goToMiddle()
      await wait(1000)
      this.leftElevator.openClaw()
      await wait(700)
      this.navigation.northTranslation(30)
      await wait(400)
      this.navigation.stop()
      await confirm()
      this.navigation.eastTranslation(30)
      await wait(0.45 * 1000)
      this.navigation.stop()
      this.leftElevator.goToOrigin()
      await wait(0.8 * 1000)
      await confirm()
      this.navigation.westTranslation(30)
      await wait(0.45 * 1000)
      this.navigation.stop()
      this.leftElevator.closeClaw()
      await wait(0.8 * 1000)
      this.leftElevator.goToTop()
      await wait(0.5 * 1000)
      await confirm()
      this.navigation.westTranslation(30)
      await wait(0.40 * 1000)
      this.navigation.stop()
      await confirm()
      this.leftElevator.goToMiddle()
      await wait(0.40 * 1000)
      this.leftElevator.openClaw()
      await confirm()
      this.navigation.eastTranslation(30)
      await wait(0.45 * 1000)
      this.navigation.stop()
      this.leftElevator.goToOrigin()
      await wait(0.8 * 1000)
      await confirm()
      this.navigation.westTranslation(30)
      await wait(0.45 * 1000)
      this.navigation.stop()
      this.leftElevator.closeClaw()
      await wait(0.8 * 1000)
      this.leftElevator.goToTop()
      await wait(0.5 * 1000)
      await confirm()
      this.navigation.westTranslation(30)
      await wait(0.40 * 1000)
      this.navigation.stop()
      await confirm()
      this.leftElevator.goToMiddle()
      await wait(0.40 * 1000)
      this.leftElevator.openClaw()
      await confirm()
      this.navigation.eastTranslation(30)
      await wait(0.45 * 1000)
      this.navigation.stop()
      this.leftElevator.goToOrigin()
      await wait(0.8 * 1000)
      await confirm()
      this.navigation.westTranslation(30)
      await wait(0.45 * 1000)
      this.navigation.stop()
      this.leftElevator.closeClaw()
      await wait(0.8 * 1000)
      this.leftElevator.goToTop()
    })
  }
}
