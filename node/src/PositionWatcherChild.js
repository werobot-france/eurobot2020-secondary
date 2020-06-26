const time = require('./Time')
const rpio = require('rpio')

let Watcher = class PositionWatcher {

  // using https://www.npmjs.com/package/rpio
  constructor() {
    this.perimeter = 60*Math.PI
    this.wheelRatio = this.perimeter/2400

    this.theta = Math.PI/2
    this.x = 0
    this.y = 0
    
    this.isTurning = false

    this.L = 103.4
    this.l = 210
    
    this.backPhaseA = 31 //6
    this.backPhaseB = 36 //16

    this.sidePhaseC = 38 //20
    this.sidePhaseD = 40 //21

    this.enabled = false
  }

  openPins() {
  }

  watch() {
    rpio.init()
    rpio.open(this.backPhaseA, rpio.INPUT)
    rpio.open(this.backPhaseB, rpio.INPUT)
    rpio.open(this.sidePhaseC, rpio.INPUT)
    rpio.open(this.sidePhaseD, rpio.INPUT)

    let ticks = [0, 0]
    let oldTicks = [0, 0]
    
    let sideState = [0, 0]
    let sideOldState = [0, 0]

    let backState = [0, 0]
    let backOldState = [0, 0]

    while (this.enabled) {
      let changed = false
      let sideFetchedState = [
        rpio.read(this.sidePhaseC),
        rpio.read(this.sidePhaseD)
      ]
      let backFetchedState = [
        rpio.read(this.backPhaseA),
        rpio.read(this.backPhaseB)
      ]
      console.log(sideFetchedState, backFetchedState)
      time.wait(500)

      if (sideFetchedState !== sideState) {
        sideState = sideFetchedState

        if (sideState[0] == sideOldState[1]) {
          ticks[0]--
        } else {
          ticks[0]++
        }
        
        sideOldState = sideState
        changed = true
      }

      if (backFetchedState !== backState) {
        backState = backFetchedState

        if (backState[0] == backOldState[1]) {
          ticks[1]--
        } else {
          ticks[1]++
        }

        backOldState = backState
        changed = true
      }

      if (ticks !== oldTicks) {
        let deltaTicks = [
          ticks[0] - oldTicks[0],
          ticks[1] - oldTicks[1]
        ]
        //console.log(deltaTicks)
        
        oldTicks = ticks

        let sideDistance = deltaTicks[0] * this.wheelRatio
        let backDistance = deltaTicks[1] * this.wheelRatio
        // if (this.isTurning) {
        //   this.theta += (sideDistance/this.l + backDistance/this.L)/2
        // } else {
          
        // }
        this.x += Math.sin(this.theta)*backDistance + Math.cos(this.theta)*sideDistance
        this.y += Math.cos(this.theta)*backDistance + Math.sin(this.theta)*sideDistance
        
        // posititon has changed, handle it ?
        console.log(this.x, this.y, this.theta)
      }
    }
  }

  start() {
    console.log('> PositionWatcher: starting...')
    this.openPins()
    this.enabled = true
    this.watch()
  }

  stop() {
    this.enabled = false
  }
}

let watcher = new Watcher()
watcher.start()