from src.DualshockThroughtNode import DualshockThroughtNode

dualshock = DualshockThroughtNode()

def onInput(label, value):
    print(label, value)
    
def onDetection(controller):
    print("python", controller)

dualshock.events.on('controller_detected', onInput)
dualshock.events.on('controller_input', onInput)

print('server started')

dualshock.startServer()

