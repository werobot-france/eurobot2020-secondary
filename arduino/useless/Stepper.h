#include <Arduino.h>

class Stepper
{
    private:
        int enablePin;
        int originSwitchPin;
        int endSwitchPin;

    public:
        Stepper(int enablePin, int originSwitchPin, int endSwitchPin);
        void enable();
        void disable();
        int getEnablePin();
};