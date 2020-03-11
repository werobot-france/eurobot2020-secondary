module.exports = class Stacker {

    constructor(params) {
        this.navigation = params.navigation
        this.leftElevator = params.leftElevator
        this.rightElevator = params.rightElevator
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

        elevator.goToMiddle()
        await this.wait(0.5)
        elevator.openClaw()

        await this.wait(0.5)

        this.navigation.eastTranslation(30)
        await this.wait(0.5)
        this.navigation.stop()
        
        await elevator.goToOrigin()
		this.navigation.westTranslation(30)
		

        await this.wait(0.55)
        this.navigation.stop()

        elevator.closeClaw()
        await this.wait(0.8)
        elevator.goToTop()
        await this.wait(1.5)
    }

    //
    // config = ['G', 'G', 'R', 'R', 'R']
    async stackRoutine(config) {
        let currentElevator = this.leftElevator
        this.rightElevator.goToTop()
        let offset = 0
        currentElevator.goToTop()
        await this.wait(0.9)
        this.navigation.westTranslation(30)
        await this.wait(0.3)
        this.navigation.stop()
        await this.takeBuos(currentElevator)
        for (var i = 1; i < 5; i++) {
            // await this.confirm('NEW BUOS? ???????????')
        	await this.wait(1)

            if (config[i] === config[i - 1]) {
                console.log('OFFSET 1')
                offset = 1
            } else if (currentElevator.getLabel() === 'left') {
                console.log('OFFSET 2 - CHOOSE LEFT')
                offset = 2
                currentElevator = this.rightElevator
            } else if (currentElevator.getLabel() === 'right') {
                console.log('OFFSET 0 - CHOOSE RIGHT')
                offset = 0
                currentElevator = this.leftElevator
            }
            //translation west de la valeur de décallage
            this.navigation.westTranslation(30)
            if (i === 4) {
                offset += 0.4
            }
            await this.wait(0.37 * offset)
            this.navigation.stop()
			await this.takeBuos(currentElevator)
			
        	await this.wait(0.7)

            // await this.confirm('END BUOS? ???????????')
        }
    }
}