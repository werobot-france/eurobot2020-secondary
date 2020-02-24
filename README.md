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

## bluetooth

rfkill unblock bluetooth