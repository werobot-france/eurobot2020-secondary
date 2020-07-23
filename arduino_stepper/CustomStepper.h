#include <Arduino.h>
#include <AccelStepper.h>

class CustomStepper
{
    private:
        int enablePin;
        int originSwitchPin;
        int endSwitchPin;
        int runningSpeed;
        bool moveTask;
        int targetPosition;
        bool speaker;
        AccelStepper stepper;

    public:
        CustomStepper(bool speaker, int dirPin, int stepPin, int enablePin, int originSwitchPin, int endSwitchPin);
        void enable();
        void disable();
        int getEnablePin();
        int getCurrentPosition();
        void loop();
        void continuous(int speed);
        void stop();
        void init();
        void goTo(int position, int speed);
        void setAcceleration(int accl);
};
