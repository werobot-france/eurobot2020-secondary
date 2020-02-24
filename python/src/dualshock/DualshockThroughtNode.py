from src.dualshock.Dualshock import Dualshock
import asyncio
import websockets
import json
import time
import subprocess
import threading

class DualshockThroughtNode(Dualshock):
    
    websocketHost = "localhost"
    websocketPort = 8000
    events = None
    websocket = None
    eventLoop = None
    
    async def serverLoop(self, websocket, path):
        while True:
            rawBody = await websocket.recv()
            parsedBody = json.loads(rawBody)

            self.websocket = websocket
            if parsedBody['t'] == "init":
                print('> DualshockThroughtNode: Initialized')

            elif parsedBody['t'] == "device":
                print('> DualshockThroughtNode: Detected')
                #self.setLed(0, 255, 255)
                print(parsedBody['d'])
                #self.events.emit('controller_detected', controller=parsedBody["d"])

            elif parsedBody['t'] == "disconnection":
                print('> DualshockThroughtNode: Disconnected')
                #self.events.emit('controller_disconnected')

            elif parsedBody['t'] == "analog_input":
                label = parsedBody['d'][0]
                value = parsedBody['d'][1]
                # map value 
                value = round((value * 2 / 255) - 1, 3)
                if label == 'lStickX': 
                    self.controllerAnalogValues['leftStickX'] = value
                elif label == 'lStickY': 
                    self.controllerAnalogValues['leftStickY'] = value
                elif label == 'rStickX': 
                    self.controllerAnalogValues['rightStickX'] = value
                elif label == 'rStickY': 
                    self.controllerAnalogValues['rightStickY'] = value
                elif label == 'r2' or label == 'l2':
                    self.controllerAnalogValues[label] = value
                
                self.events.emit('analog_input', values=self.controllerAnalogValues)
                
            elif parsedBody["t"] == "digital_input":
                label = parsedBody['d'][0]
                value = parsedBody['d'][1]
                #print(label, value)
                changed = False
                if label == 'r3':
                    self.controllerDigitalValues['rightStick'] = value
                    changed = True
                elif label == 'l3':
                    self.controllerDigitalValues['leftStick'] = value
                    changed = True
                elif label == 'start':
                    self.controllerDigitalValues['options'] = value
                    changed = True
                elif label == 'select':
                    self.controllerDigitalValues['share'] = value
                    changed = True
                elif label != 'a' and label != 'b' and label != 'x' and label != 'y':
                    self.controllerDigitalValues[label] = value
                    changed = True
                
                if changed:
                    self.events.emit('digital_input', values=self.controllerDigitalValues)
                    changed = False
    
    def startNodeJs(self):
        subprocess.Popen(["node", "dualshock_node/dualshock.js"])

    def setLed(self, r, g, b):
        print('LED', r, g, b)
        asyncio.ensure_future(self.websocket.send(json.dumps({'t': 'led', 'd': [r, g, b]})))
        
    def setRumble(self, left, right):
        print('RUMBLE', left, right)
        asyncio.ensure_future(self.websocket.send(json.dumps({'t': 'rumble_set', 'd': [left, right]})))
    
    def start(self):
        print('dualshock: socket server started')
        self.setDefaultControllerValues()
        self.startNodeJs()
        self.eventLoop = asyncio.get_event_loop()
        self.eventLoop.run_until_complete(websockets.serve(self.serverLoop, self.websocketHost, self.websocketPort))
        self.eventLoop.run_forever()