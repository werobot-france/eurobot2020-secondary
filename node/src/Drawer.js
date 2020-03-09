module.exports = class Drawer {
    constructor(params) {
        this.pwmInterface = params.pwmInterface
        this.arduinoInterface = params.arduinoInterface
        this.squeezerSlot = 7
        this.drawerOpened = false
        this.squeezerOpened = false
    }

    async goToBack() {
        if (this.squeezerOpened) {
            console.warn("> WARNING: The squeezer will be completly closed before closing the drawer")

            this.completlySqueeze()

            setTimeout(async () => {
                await this.arduinoInterface.sendCommand('DRAWER_GO_TO_BACK', [200])
            }, 700)
        } else {
            this.completlySqueeze()
            await this.arduinoInterface.sendCommand('DRAWER_GO_TO_BACK', [200])
        }
        this.drawerOpened = false
    }

    async goToFront() {
        await this.arduinoInterface.sendCommand('DRAWER_GO_TO_FRONT', [200])
        this.drawerOpened = true
    }

    toggle() {
        if (this.drawerOpened) {
            this.goToBack()
        } else {
            this.goToFront()
        }
    }
    
    closeSqueezer() {
        this.pwmInterface.setAngle(this.squeezerSlot, 175)
        this.squeezerOpened = false

        console.log('squeezer closed')
    }
    
    openSqueezer() {
        if (!this.drawerOpened) {
            console.warn("> WARNING: Can't open squeezer because the drawer is closed")
        } else {
            this.pwmInterface.setAngle(this.squeezerSlot, 90)
            this.squeezerOpened = true
            console.log('squeezer opened')
        }
    }

    completlySqueeze() {
        this.pwmInterface.setAngle(this.squeezerSlot, 180)
        console.log('COMPLETLY Squeeze')
        this.squeezerOpened = false
    }

    toggleSqueezer() {
        if (!this.squeezerOpened) {
            this.openSqueezer()
        } else {
            this.closeSqueezer()
        }
    }
}