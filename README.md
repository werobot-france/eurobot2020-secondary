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


- routine attraper goblet
    - si il est pas au bon niveau, ce mettre au niveau haut
    - ouvrir pince
    - descendre au niveau eceuil
    - fermer pince
    - se mettre au niveau haut
- routine
