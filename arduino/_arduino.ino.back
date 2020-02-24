#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <AccelStepper.h>

/**
 * Command interface
 **/
String command = "";
String commandName = "";
int commandParam1 = 0;
int commandParam2 = 0;
int commandParam3 = 0;
int commandParam4 = 0;

/**
 * Stepper interface
 **/
#define motorInterfaceType 1

/* Drawer */
#define dirDrawer 12
#define stepDrawer 11
#define enableDrawer 10

/* 1 Right elevator (middle stepper) */
#define dirRightElevator 5
#define stepRightElevator 4
#define enableRightElevator 3

/* 0 Left elevator */
#define dirLeftElevator 2
#define stepLeftElevator 6
#define enableLeftElevator 7

/* Limit switches */
#define lsBackDrawer 14 // BACK DRAWER
#define lsFrontDrawer 15 // FRONT DRAWER
#define lsLeftElevator 8 // LEFT ELEVATOR
#define lsRightElevator 9 // RIGHT ELEVATOR

AccelStepper drawer = AccelStepper(motorInterfaceType, stepDrawer, dirDrawer);
AccelStepper leftElevator = AccelStepper(motorInterfaceType, stepLeftElevator, dirLeftElevator);
AccelStepper rightElevator = AccelStepper(motorInterfaceType, stepRightElevator, dirRightElevator);

int leftElevatorPosition = 0;
int rightElevatorPosition = 0;

void drawerGoToBack() {
  digitalWrite(enableDrawer, LOW);
  while (digitalRead(lsBackDrawer) == HIGH) {
    drawer.setSpeed(200); // back is positive speed = 100
    drawer.runSpeed();
  }
  digitalWrite(enableDrawer, HIGH);
  drawer.setCurrentPosition(0);
}

void drawerGoToFront() {
  digitalWrite(enableDrawer, LOW);
  while (digitalRead(lsFrontDrawer) == HIGH) {
    drawer.setSpeed(-200); // front is negative
    drawer.runSpeed();
  }
  digitalWrite(enableDrawer, HIGH);
}

// void elevatorGoToOrigin(int elevator) {
//   AccelStepper stepper;
//   int switchPin;
//   int enablePin;
//   if (elevator == 0) {
//     stepper = leftElevator;
//     switchPin = lsLeftElevator;
//     enablePin = enableLeftElevator;
//   }
//   if (elevator == 1) {
//     stepper = rightElevator;
//     switchPin = lsRightElevator;
//     enablePin = enableRightElevator;
//   }
//   digitalWrite(enablePin, LOW);
//   while (digitalRead(switchPin) == HIGH) {
//     stepper.setSpeed(300); // origin is negative
//     stepper.runSpeed();
//   }
// }

/*
void _delay(float seconds) {
  long endTime = millis() + seconds * 1000;
  while (millis() < endTime)_loop();
}
*/

void setup() {
  Serial.begin(9600);

  pinMode(lsBackDrawer, INPUT);
  pinMode(lsFrontDrawer, INPUT);
  pinMode(lsLeftElevator, INPUT);
  pinMode(lsRightElevator, INPUT);

  pinMode(enableDrawer, OUTPUT);
  pinMode(enableLeftElevator, OUTPUT);
  pinMode(enableRightElevator, OUTPUT);
  
  digitalWrite(enableDrawer, HIGH);
  digitalWrite(enableLeftElevator, HIGH);
  digitalWrite(enableRightElevator, HIGH);
  
  leftElevator.setMaxSpeed(1000);
  rightElevator.setMaxSpeed(1000);
  drawer.setMaxSpeed(1000);

  Serial.println("SETUP: Ready");
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    if (command != "") {
      commandName = command.substring(0, command.indexOf("#"));

      // Parse command arguments (1, 2, 3)
      String raw1 = command.substring(command.indexOf("#") + 1, command.length());
      if (raw1 != command) {
        commandParam1 = raw1.substring(0, raw1.indexOf("#")).toInt();

        String raw2 = raw1.substring(raw1.indexOf("#") + 1, raw1.length());
        //        Serial.println(raw2);

        if (raw2 != raw1) {
          if (raw2.indexOf("#") != -1) {
            commandParam2 = raw2.substring(0, raw2.indexOf("#")).toInt();

            String raw3 = raw2.substring(raw2.indexOf("#") + 1, raw2.length());
            if (raw3 != raw2) {
              if (raw3.indexOf("#") != -1) {
                commandParam3 = raw3.substring(0, raw3.indexOf("#")).toInt();
                commandParam4 = raw3.substring(raw3.indexOf("#") + 1, raw3.length()).toInt();
              } else {
                commandParam3 = raw3.substring(0, raw3.length()).toInt();
              }
            }
          } else {
            commandParam2 = raw2.substring(0, raw2.length()).toInt();
          }
        }
      }

      //Serial.println(commandName);
      if (commandName == "RESET") {
        Serial.println("L: Reset!");

      } else if (commandName == "PING") {
        Serial.println("L: Pong!");

      } else if (commandName == "DRAWER_GO_TO_BACK") {
        drawerGoToBack();
        Serial.println("DRAWER_GO_TO_BACK: Done");
      } else if (commandName == "DRAWER_GO_TO_FRONT") {
        drawerGoToFront();
        Serial.println("DRAWER_GO_TO_FRONT: Done");
      } else if (commandName == "ELEVATOR_GO_TO") {
        /**
         * Command ELEVATOR_GO_TO
         **/

        /**
         * -850 step maximum
         **/
        int elevator = commandParam1;
        AccelStepper stepper;
        int switchPin;
        int enablePin;
        if (elevator == 0) {
            stepper = leftElevator;
            switchPin = lsLeftElevator;
            enablePin = enableLeftElevator;
            stepper.setCurrentPosition(leftElevatorPosition);
        }
        if (elevator == 1) {
            stepper = rightElevator;
            switchPin = lsRightElevator;
            enablePin = enableRightElevator;
            stepper.setCurrentPosition(rightElevatorPosition);
        }
        Serial.print("ELEVATOR_GO_TO: Start with ");
        Serial.print(stepper.currentPosition());
        Serial.println(" position");

        int speed = commandParam3;
        if (speed == 0) {
            speed = 300; // default speed is 300
        }

        // enable the stepper
        digitalWrite(enablePin, LOW);

        int targetPosition = commandParam2;
        if (targetPosition == 0) {
            while (digitalRead(switchPin) == HIGH) {
                stepper.setSpeed(speed); // origin is negative
                stepper.runSpeed();
            }
            stepper.setCurrentPosition(0);
        } else {
            while(stepper.currentPosition() != targetPosition)
            {
                stepper.setSpeed(speed);
                stepper.runSpeed();
            }
        }

        // disable the stepper
        digitalWrite(enablePin, HIGH);

        if (elevator == 0) {
            leftElevatorPosition = stepper.currentPosition();
        }
        if (elevator == 1) {
            rightElevatorPosition = stepper.currentPosition();
        }

        Serial.print("ELEVATOR_GO_TO: Done with ");
        Serial.print(stepper.currentPosition());
        Serial.println(" position");
      } else if (commandName == "CMD") {
        Serial.print("CMD: ");
        Serial.print(commandParam1);
        Serial.print("  ");
        Serial.print(commandParam2);
        Serial.print("  ");
        Serial.print(commandParam3);
        Serial.print("  ");
        Serial.println(commandParam4);
      }
      else {
        Serial.println("E: invalid commandName");
      }
      commandParam1 = 0;
      commandParam2 = 0;
      commandParam3 = 0;
      commandParam4 = 0;
    }
  }
}