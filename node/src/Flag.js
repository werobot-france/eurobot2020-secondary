// slot #4

module.exports = class Flags {
    constructor(params) {
        this.pwmInterface = params.pwmInterface
        this.servoSlot = params.servoSlot
        this.flagsOpened = false
    }

    open() {
        console.log('> Flags: opening')

        this.pwmInterface.setAngle(this.servoSlot, 180)

        this.flagsOpened = true
    }

    close() {
        console.log('> Flags: closing')

        this.pwmInterface.setAngle(this.servoSlot, 0)

        this.flagsOpened = false
    }

    toggle() {
        if (this.flagsOpened) {
            this.close()
        } else {
            this.open()
        }
    }

    startTimer() {
        console.log('> Flags: Timer started, set to 95 seconds')
        setTimeout(() => {
            console.log('> Flags: 5 SECONDS BEFORE END OF THE MATCH')
            this.open()
        }, 95 * 1000)
    }
}