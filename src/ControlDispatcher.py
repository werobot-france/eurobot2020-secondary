class ControlDispatcher:
    
    minSpeed = 25
    currentSpeed = 25
    isL2Triggered = False
    
    def __init__(self, dualshock, navigation):
        dualshock.on('analog_input', self.onAnalog)
        dualshock.on('digital_input', self.onAnalog)
        self.navigation = navigation
        return
    
    # équivalent de la fonction map() de arduino
    def mappyt(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

    # fonction esc pour une vitesse de moteur de -100 à 100()
    def convertSpeedToEsc(self, speed):
        return round(self.mappyt(speed, 0, 100, 307, 410))
    
    def onAnalog(self, values):
        seuil = 0.1

        # lStickX = data['lStickX'] - 127
        # lStickY = -(data['lStickY'] - 127)
        # rStickX = data['rStickX'] / 127 - 1
        # rStickY = -(data['rStickY'] / 127 - 1)
        # l2 = data['l2'] / 255  # accélération
        # #r2 = data['r2'] / 255 # accélération

        # pygame version
        lStickX = values['leftStickX']
        lStickY = -values['leftStickY']
        rStickX = values['rightStickX']
        rStickY = -values['rightStickY']
        l2 = values['l2']  # accélération

        #print([rStickX, rStickY])

        # and
        # (abs(l2+1) <= seuil or abs(l2) <= seuil) and
        # (abs(r2+1) <= seuil or abs(r2) <= seuil)
        if (abs(lStickX) <= seuil and
            abs(lStickY) <= seuil and
            abs(rStickX) <= seuil and
                abs(rStickY) <= seuil):
            print("reset")
            self.stopAll()
        else:
            if self.isL2Triggered:
                self.currentSpeed = self.mappyt(l2, -1, 1, 0, 1) * 100
            else:
                self.currentSpeed = self.minSpeed

            # if lStickX == -1:
            #     self.currentSpeed = self.minSpeed
            # elif lStickX != 0 :
            #     self.currentSpeed = self.mappyt(lStickX, -1, 1, 0, 1) * 100
            #     #print("lStickX = {0} et vt = {1}".format(lStickX,vt))

            # r stick ?
            if not (abs(rStickX) <= seuil and
                    abs(rStickY) <= seuil):
                if rStickY < 0.5 * rStickX and rStickY >= -0.5 * rStickX:
                    self.navigation.eastTranslation(self.currentSpeed)
                if rStickY > 0.5 * rStickX and rStickY <= 2 * rStickX:
                    self.navigation.northEastTranslation(self.currentSpeed)
                if rStickY > 2 * rStickX and rStickY >= -2 * rStickX:
                    self.navigation.northTranslation(self.currentSpeed)
                if rStickY < -2 * rStickX and rStickY >= -0.5 * rStickX:
                    self.navigation.northWestTranslation(self.currentSpeed)
                if rStickY < -0.5 * rStickX and rStickY >= 0.5 * rStickX:
                    self.navigation.westTranslation(self.currentSpeed)
                if rStickY < 0.5 * rStickX and rStickY >= 2 * rStickX:
                    self.navigation.southWestTranslation(self.currentSpeed)
                if rStickY < 2 * rStickX and rStickY <= -2 * rStickX:
                    self.navigation.southTranslation(self.currentSpeed)
                if rStickY > -2 * rStickX and rStickY <= -0.5 * rStickX:
                    self.navigation.southEastTranslation(self.currentSpeed)

            if lStickY < 0.5 * lStickX and lStickY >= -0.5 * lStickX:
                self.clockwiseRotation(self.currentSpeed)
            if lStickY < -0.5 * lStickX and lStickY >= 0.5 * lStickX:
                self.antiClockwiseRotation(self.currentSpeed)
            print('end analog input event')
            
    def onDigital(self, values):
        print(values)
        
        if values['ps']:
            self.navigation.stopAll()
        self.isL2Triggered = values['l2']
