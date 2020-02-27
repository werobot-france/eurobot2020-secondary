#include "Stepper.h"

Stepper::Stepper(int enablePin, int originSwitchPin, int endSwitchPin = -1)
{
    Stepper::enablePin = enablePin;
    Stepper::originSwitchPin = originSwitchPin;
    Stepper::endSwitchPin = endSwitchPin;
}

void Stepper::disable()
{
    digitalWrite(Stepper::enablePin, 1);
}

void Stepper::enable()
{
    digitalWrite(Stepper::enablePin, 0);
}

int Stepper::getEnablePin()
{
    return Stepper::enablePin;
}