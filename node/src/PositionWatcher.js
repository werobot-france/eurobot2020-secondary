const rpio = require('rpio')

module.exports = class PositionWatcher {

  // using https://www.npmjs.com/package/rpio
  constructor() {
    this.perimeter = 60*Math.PI
    this.wheelRatio = this.perimeter/2400

    this.theta = Math.PI/2
    this.x = 0
    this.y = 0
    
    this.ticks = [0, 0]
    this.oldTicks = [0, 0]
    
    this.sideState = [0, 0]
    this.sideOldState = [0, 0]

    this.backState = [0, 0]
    this.backOldState = [0, 0]

    this.isTurning = false

    this.L = 103.4
    this.l = 210
    
    this.backPhaseA = 17 
    this.backPhaseB = 27

    this.sidePhaseC = 22
    this.sidePhaseD = 23

    this.enabled = false
  }

  openPins() {
    rpio.open(this.backPhaseA, rpio.INPUT)
    rpio.open(this.backPhaseB, rpio.INPUT)
    rpio.open(this.sidePhaseC, rpio.INPUT)
    rpio.open(this.sidePhaseD, rpio.INPUT)

    //rpio.read(15)
  }

  watchTicks() {
    while (this.enabled) {
      let sideFetchedState = [
        rpio.read(this.sidePhaseC),
        rpio.read(this.sidePhaseD)
      ]
      let backFetchedState = [
        rpio.read(this.backPhaseA),
        rpio.read(this.backPhaseB)
      ]

      if (sideFetchedState !== this.sideState) {
        this.sideState = sideFetchedState

        if (this.sideState[0] == this.sideOldState[1]) {
          this.ticks[0]--
        } else {
          this.ticks[0]++
        }
        
        this.sideOldState = this.sideState
      }

      if (backFetchedState !== this.backState) {
        this.backState = backFetchedState

        if (this.backState[0] == this.backOldState[1]) {
          this.ticks[1]--
        } else {
          this.ticks[1]++
        }

        this.backOldState = this.backState
      }
    }
  }

  watchPosititon() {
    while (this.enabled) {
      // LEFT = SIDE
      // RIGHT = BACK
      if (this.ticks !== this.oldTicks) {
        let deltaTicks = [
          this.ticks[0] - this.oldTicks[0],
          this.ticks[1] - this.oldTicks[1]
        ]
        this.oldTicks = this.ticks
        let sideDistance = deltaTicks[0] * this.wheelRatio
        let backDistance = deltaTicks[1] * this.wheelRatio
        if (this.isTurning) {
          this.theta += (sideDistance/this.l + backDistance/this.L)/2
        } else {
          this.x += Math.sin(this.theta)*backDistance + Math.cos(this.theta)*sideDistance
          this.y += Math.cos(this.theta)*backDistance + Math.sin(this.theta)*sideDistance
        }
        // posititon has changed, handle it ?
      }
      // wait ?
    }
  }

}