#include "CustomStepper.h"

/**
 * originSwitchPin is the positive side
 * endSwitchPin is the negative side
 * */
CustomStepper::CustomStepper(int dirPin, int stepPin, int enablePin, int originSwitchPin, int endSwitchPin = -1)
{
    this->runningSpeed = 0;
    this->enablePin = enablePin;
    this->originSwitchPin = originSwitchPin;
    this->endSwitchPin = endSwitchPin;
    this->stepper = AccelStepper(1, stepPin, dirPin);
}

void CustomStepper::init()
{
    pinMode(this->enablePin, OUTPUT);
    pinMode(this->originSwitchPin, INPUT);
    if (this->endSwitchPin != -1) {
        pinMode(this->endSwitchPin, INPUT);
    }
    this->disable();
    this->stepper.setMaxSpeed(1000);
}

void CustomStepper::disable()
{
    digitalWrite(this->enablePin, 1);
}

void CustomStepper::enable()
{
    digitalWrite(this->enablePin, 0);
}

int CustomStepper::getEnablePin()
{
    return this->enablePin;
}

void CustomStepper::loop()
{
   if (this->runningSpeed != 0) {
        this->stepper.runSpeed();
        if (this->runningSpeed > 0 && digitalRead(this->originSwitchPin) == 0) {
            this->disable();
            this->runningSpeed = 0;

            Serial.println("CUSTOM_STEPPER: Go to origin done");
        } else if (this->endSwitchPin != -1 && this->runningSpeed < 0 && digitalRead(this->endSwitchPin) == 0) {
            this->disable();
            this->runningSpeed = 0;

            Serial.println("CUSTOM_STEPPER: Go to end done");
        }
   }
}

void CustomStepper::continuous(int speed)
{
    this->runningSpeed = speed;
    this->enable();
    this->stepper.setSpeed(speed);
}

void CustomStepper::stop()
{
    this->runningSpeed = 0;
    this->disable();
}