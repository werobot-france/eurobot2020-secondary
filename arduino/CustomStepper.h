#include <Arduino.h>
#include <AccelStepper.h>

class CustomStepper
{
    private:
        int enablePin;
        int originSwitchPin;
        int endSwitchPin;
        int runningSpeed;
        AccelStepper stepper;

    public:
        CustomStepper(int dirPin, int stepPin, int enablePin, int originSwitchPin, int endSwitchPin);
        void enable();
        void disable();
        int getEnablePin();
        void loop();
        void continuous(int speed);
        void stop();
        void init();
};
