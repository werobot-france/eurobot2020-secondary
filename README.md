# eurobot2020-main

## python lib requirements

### dualshock via node

- PyEventEmitter
- websockets

## Architecture

- interface hardware-software pour l'assemblage ascenseur
    - ouvrir pince
    - fermer pince
    - niveau supra eceuil
    - niveau attrape eceuil
    - niveau depilage rat/bas
    - niveau depilage haut
    - init pince
        - go to direction and click with end switch
        - close pince

- interface hardware-software pour l'assemblage tiroir
    - sortir tiroir
    - rentrer tiroir
    - init tiroir
        - go to endswitch

- routine attraper goblet (une routine par ascenseur)
    - si il est pas au bon niveau, se mettre au niveau haut
    - ouvrir pince
    - descendre au niveau eceuil
    - fermer pince
    - se mettre au niveau haut

- routine dépiller (une routine par ascenseur)
    - s'il il n'est pas ouvert, ouvrir le tiroir
    - s'il il est pas au bon niveau, se mettre au niveau depiller bas
    - ouvrir pince
    - se mettre au niveau depiller haut
    - fermer pince
    - fermer squeezer
    - se mettre au niveau deplier supra haut
    - ouvrir squeezer
    - (ranger tiroir)

## Communication protocol via Serial:

- 0: Drawer stepper
- 1: Left/Front Elevator
- 2: Right/Back Elevator

- positiveDirection: if true, step are positives

- STEPPERS
    - GO_TO_ORIGIN(int stepperId, bool positiveDirection)
    - GO_TO(int stepperId, int position)
    - DISABLE_ALL()
- LED
    - SET_FLASHING_MODE(array pulses)
    - DISABLE()
- BUTTON (will receive an event when button at falling edge of the push button: with the time)
    - ENABLE()
    - DISABLE()
- SCREEN
    - SET_FIRST_LINE()
    - SET_SECOND_LINE()
    - CLEAR()
    - ENABLE()
    - DISABLE()

## bluetooth

rfkill unblock bluetooth

## TODO

- disable feature on elevator
- disable elevator until go to origin to prevent steps jumps