module.exports = class UnStacker {

    constructor(params) {
        this.navigation = params.navigation
        this.leftElevator = params.leftElevator
        this.rightElevator = params.rightElevator
        this.drawer = params.drawer
    }

    wait(timeout) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve()
            }, timeout * 1000)
        })
    }
    
    confirm(label = '') {
        return new Promise((resolve) => {
            var standard_input = process.stdin
            standard_input.setEncoding('utf-8')
            console.log("Confirm action? " + label)
            standard_input.removeAllListeners()
            standard_input.on('data', () => {
                resolve()
            })
        })
    }

    async takeBuos(elevator) {
        this.drawer.openSqueezer()
        await this.wait(0.8)
        await elevator.goToOrigin()
        await this.wait(0.3)
        elevator.openClaw()
        await this.wait(1)
        await this.confirm('Close squeezer')
        this.drawer.closeSqueezer()
        await this.confirm('GO TO UNSTACK POS')
        await elevator.goToUnStackPos() // -96
        await this.confirm('CLOSE CLAW')
        elevator.closeClaw()
        await this.confirm('GO TO TOP')
        elevator.goToUnStackPos()
        await this.wait(0.4)
        elevator.goToMiddle()
        await this.wait(0.4)
        elevator.goToTop()
        await this.wait(0.5)
        console.log('DONE UNTAKE BUOS')
    }

    async unStackRoutine() {
        // we asume that the robot is the good position
        await this.confirm('> START UNSTACK ROUTINE ?')
        let elevator = this.rightElevator
        await this.drawer.goToFront()
        this.drawer.openSqueezer()
        await this.wait(0.5)
        this.takeBuos(elevator)
        this.takeBuos(elevator)

        //await elevator.goToOrigin()
    }
}