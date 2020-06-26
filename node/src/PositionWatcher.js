const time = require('./Time')
const rpio = require('rpio')
const EventEmitter = require('events')
const Fiber = require('fibers')

module.exports = class PositionWatcher extends EventEmitter {

  // using https://www.npmjs.com/package/rpio
  constructor() {
    super()
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
    
    this.backPhaseA = 6
    this.backPhaseB = 16

    this.sidePhaseC = 20
    this.sidePhaseD = 21

    this.enabled = false
  }

  openPins() {
    rpio.init({ mapping: 'gpio' })
    rpio.open(this.backPhaseA, rpio.INPUT)
    rpio.open(this.backPhaseB, rpio.INPUT)
    rpio.open(this.sidePhaseC, rpio.INPUT)
    rpio.open(this.sidePhaseD, rpio.INPUT)

    //rpio.read(15)
  }

  watchTicks() {
    return Fiber(() => {
      Fiber.yield(0)
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
        //console.log(sideFetchedState, backFetchedState)

        if (sideFetchedState !== this.sideState) {
          this.sideState = sideFetchedState

          if (this.sideState[0] == this.sideOldState[1]) {
            this.ticks[0]--
          } else {
            this.ticks[0]++
          }
          
          this.sideOldState = this.sideState
          changed = true
        }

        if (backFetchedState !== this.backState) {
          this.backState = backFetchedState

          if (this.backState[0] == this.backOldState[1]) {
            this.ticks[1]--
          } else {
            this.ticks[1]++
          }

          this.backOldState = this.backState
          changed = true
        }

        if (changed) {
          Fiber.yield(this.ticks)
        }
      }
    }).run.bind(this)
  }

  async watchPosititon(fetchTicks) {
    let oldTicks = [0, 0]
    while (this.enabled) {
      // LEFT = SIDE
      // RIGHT = BACK
      let ticks = fetchTicks()
      if (ticks !== oldTicks) {
        let deltaTicks = [
          ticks[0] - oldTicks[0],
          ticks[1] - oldTicks[1]
        ]
        console.log(deltaTicks)
        oldTicks = ticks
        // let sideDistance = deltaTicks[0] * this.wheelRatio
        // let backDistance = deltaTicks[1] * this.wheelRatio
        // // if (this.isTurning) {
        // //   this.theta += (sideDistance/this.l + backDistance/this.L)/2
        // // } else {
          
        // // }
        // this.x += Math.sin(this.theta)*backDistance + Math.cos(this.theta)*sideDistance
        // this.y += Math.cos(this.theta)*backDistance + Math.sin(this.theta)*sideDistance
        // // posititon has changed, handle it ?
        // this.emit('positionUpdated', this.x, this.y, this.theta)
      }
      // wait ?
      await time.wait(10)
    }
  }

  init() {
    this.openPins()
    this.enabled = true
    console.log('> PositionWatcher: starting...')
    let ticks = this.watchTicks()
    console.log('> tick watcher started')
    this.watchPosititon(ticks)
  }

  stop() {
    this.enabled = false
  }
} 