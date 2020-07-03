const child_process = require('child_process')
const time = require('./Time')

module.exports = class Navigation {

  constructor(pwmInterface, positionWatcher) {
    this.escSlots = {
      frontLeft: 15,
      frontRight: 12,
      backLeft: 14,
      backRight: 13
    }
    this.pwmInterface = pwmInterface
    this.positionWatcher = positionWatcher
  }

  setSpeed(values) {
    console.log(values)
    Object.keys(values).forEach(i => {
      this.pwmInterface.setEsc(this.escSlots[i], values[i])
    })
  }

  eastTranslation(speed) {
    this.setSpeed({
      frontLeft: speed,
      frontRight: speed,
      backLeft: speed,
      backRight: speed
    })
  }

  southTranslation(speed) {
    this.northTranslation(-speed)
  }

  northTranslation(speed) {
    this.setSpeed({
      frontLeft: speed,
      frontRight: -speed,
      backLeft: -speed,
      backRight: speed
    })
  }

  westTranslation(speed) {
    this.eastTranslation(-speed)
  }

  clockwiseRotation(speed) {
    this.setSpeed({
      frontLeft: speed,
      frontRight: speed,
      backLeft: -speed,
      backRight: -speed
    })
  }

  antiClockwiseRotation(speed) {
    this.clockwiseRotation(-speed)
  }

  northEastTranslation(speed) {
    this.setSpeed({
      'frontLeft': speed,
      'frontRight': 0,
      'backLeft': 0,
      'backRight': speed
    })
  }

  southWestTranslation(speed) {
    this.northEastTranslation(-speed)
  }

  northWestTranslation(speed) {
    this.setSpeed({
      'frontLeft': 0,
      'frontRight': speed,
      'backLeft': speed,
      'backRight': 0
    })
  }

  southEastTranslation(speed) {
    this.northWestTranslation(-speed)
  }

  setSpeedFromAngle(angle, speed) {
    let generateCoeffs = a => {
      return Math.cos(Math.abs(angle - a))
    }
  
    let eastCoef       =  generateCoeffs(0)
    //let northEastCoef  =  generateCoeffs(-45)
    let northCoef      =  generateCoeffs(Math.PI/2)
    //let northWestCoef  =  generateCoeffs(45)
    let westCoef       =  generateCoeffs(Math.PI)
    //let southWestCoef  =  generateCoeffs(135)
    let southCoef      =  generateCoeffs(-Math.PI/2)
    //let southEastCoef  =  generateCoeffs(-135)
    
    // let east =      [eastCoef, eastCoef, eastCoef, eastCoef]
    // let northEast = [northEastCoef, 0, 0, northEastCoef]
    // let north =     [northCoef, -northCoef, -northCoef, northCoef]
    // let northWest = [0, northWestCoef, northWestCoef, 0]
    // let west =      [-westCoef, -westCoef, -westCoef, -westCoef]
    // let southWest = [-southWestCoef, 0, 0, -southWestCoef]
    // let south =     [-southCoef, southCoef, southCoef, -southCoef]
    // let southEast = [0, -southEastCoef, -southEastCoef, 0]
  
    let cmds = [
      [eastCoef, eastCoef, eastCoef, eastCoef],
      //[northEastCoef, 0, 0, northEastCoef],
      [northCoef, -northCoef, -northCoef, northCoef],
      //[0, northWestCoef, northWestCoef, 0],
      [-westCoef, -westCoef, -westCoef, -westCoef],
      //[-southWestCoef, 0, 0, -southWestCoef],
      [-southCoef, southCoef, southCoef, -southCoef],
      //[0, -southEastCoef, -southEastCoef, 0]
    ]
  
    let motorsSpeed = []
    for (var n = 0; n < 4; n++) {
      let sum = 0
      for (var i = 0; i < cmds.length; i++) {
        sum += cmds[i][n] * speed
      }
      motorsSpeed.push(parseFloat((sum / cmds.length * 2).toFixed(3)))
    }
    console.log(motorsSpeed)
    this.setSpeed({
      frontLeft: motorsSpeed[0],
      frontRight: motorsSpeed[1],
      backLeft: motorsSpeed[2],
      backRight: motorsSpeed[3],
    })
  }

  goTo(targetX, targetY, speed = 20, threadhold = 200) {
    return new Promise((resolve) => {
      
      let angle = Math.atan2(targetX, targetY)

      console.log(`> Navigation: going to (x: ${targetX}, y: ${targetY}) with a angle of ${angle * 180/Math.PI} deg`)

      // this.position.on('positionUpdated', (x, y, theta) => {
      //   console.log(x, y, theta)
      // })
      let watcher = child_process.spawn("python3", ["PositionWatcher.py", "-T"])
  
      watcher.stdout.on('data', d => {
        let content = d.toString()
        if (content.indexOf("ack") !== "a") {
          console.log("> Navigation: Posititon watcher python has loaded the target positions")
        }
        console.log(content)
        if (content.indexOf("done") !== -1) {
          console.log("> Navigation: Done!")
          resolve()
        }
      })

      watcher.stdin.write(targetX.toString() + ";" + targetY.toString() + ";" + threadhold.toString() + "\n")
  
      this.setSpeedFromAngle(angle, speed)
    })
  }

  stop() {
    this.setSpeed({
      'frontLeft': 0,
      'frontRight': 0,
      'backLeft': 0,
      'backRight': 0
    })
  }
}
