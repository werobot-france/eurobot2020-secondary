#include "CustomStepper.h"

/**
 * originSwitchPin is the positive side
 * endSwitchPin is the negative side
 * */
CustomStepper::CustomStepper(bool speaker, int dirPin, int stepPin, int enablePin, int originSwitchPin, int endSwitchPin = -1)
{
    this->runningSpeed = 0;
    this->speaker = speaker;
    this->enablePin = enablePin;
    this->originSwitchPin = originSwitchPin;
    this->endSwitchPin = endSwitchPin;
    this->stepper = AccelStepper(1, stepPin, dirPin);
    this->moveTask = true;
}

void CustomStepper::init()
{
    pinMode(this->enablePin, OUTPUT);
    pinMode(this->originSwitchPin, INPUT);
    if (this->endSwitchPin != -1) {
        pinMode(this->endSwitchPin, INPUT);
    }
    this->disable();
    this->stepper.setMaxSpeed(400);
    this->stepper.setAcceleration(10000);
    this->moveTask = false;
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
    if (this->moveTask) {
        this->stepper.run();
        if (this->stepper.currentPosition() == this->targetPosition) {
            if (this->speaker) {
                Serial.println("CUSTOM_STEPPER: Go to done");
            }
            this->targetPosition = 0;
            this->moveTask = false;
        }
    } else {
        this->stepper.runSpeed();
    }
    if (this->runningSpeed != 0) {
        // Serial.println(digitalRead(this->originSwitchPin));
        // if (this->runningSpeed > 0 && digitalRead(this->originSwitchPin) == 0) {
            
        // } else if (this->endSwitchPin != -1 && this->runningSpeed < 0 && digitalRead(this->endSwitchPin) == 0) {
        //     this->disable();
        //     this->runningSpeed = 0;
        //     this->stepper.setSpeed(0);

        //     Serial.println("CUSTOM_STEPPER: Go to end done");
        // }
        if (digitalRead(this->originSwitchPin) == 0) {
            this->disable();
            this->runningSpeed = 0;

            //Serial.println(this->stepper.currentPosition());

            this->stepper.setCurrentPosition(0);
            this->stepper.setSpeed(0);

            if (this->speaker) {
                Serial.println("CUSTOM_STEPPER: Go to origin done");
            }
        }
    }
}

void CustomStepper::continuous(int speed)
{
    this->moveTask = false;
    this->runningSpeed = speed;
    this->enable();
    this->stepper.setSpeed(speed);
}

void CustomStepper::goTo(int position, int speed)
{
    this->runningSpeed = 0;
    this->enable();
    this->moveTask = true;
    this->targetPosition = position;
    this->stepper.setSpeed(speed);
    this->stepper.moveTo(position);
}

int CustomStepper::getCurrentPosition()
{
    return this->stepper.currentPosition();
}

void CustomStepper::stop()
{
    this->runningSpeed = 0;
    this->disable();
}

void CustomStepper::setAcceleration(int accl)
{
    this->stepper.setAcceleration(accl);
}