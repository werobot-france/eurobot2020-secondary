#include <AccelStepper.h>

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

void drawerGoToBack() {
  digitalWrite(enableDrawer, LOW);
  while (digitalRead(lsBackDrawer) == HIGH) {
    drawer.setSpeed(100); // back is positive
    drawer.runSpeed();
  }
  digitalWrite(enableDrawer, HIGH);
}

void drawerGoToFront() {
  digitalWrite(enableDrawer, LOW);
  while (digitalRead(lsFrontDrawer) == HIGH) {
    drawer.setSpeed(-100); // front is negative
    drawer.runSpeed();
  }
  digitalWrite(enableDrawer, HIGH);
}

void elevatorGoToOrigin(int elevator) {
  AccelStepper stepper;
  int switchPin;
  int enablePin;
  if (elevator == 0) {
    stepper = leftElevator;
    switchPin = lsLeftElevator;
    enablePin = enableLeftElevator;
  }
  if (elevator == 1) {
    stepper = rightElevator;
    switchPin = lsRightElevator;
    enablePin = enableRightElevator;
  }
  digitalWrite(enablePin, LOW);
  while (digitalRead(switchPin) == HIGH) {
    stepper.setSpeed(300); // origin is negative
    stepper.runSpeed();
  }
}

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

  //stepper.setCurrentPosition(0);
  /*while(stepper.currentPosition() != 400)
  {
    stepper.setSpeed(200);
    stepper.runSpeed();
  }*/
  Serial.println("READY");
  delay(2000);

  drawerGoToBack();
  delay(2000);
  drawerGoToFront();

  delay(2000);

  elevatorGoToOrigin(0);
  delay(500);
  elevatorGoToOrigin(1);
}

void loop() {
}
