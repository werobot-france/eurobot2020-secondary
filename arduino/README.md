# Arduino code

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
