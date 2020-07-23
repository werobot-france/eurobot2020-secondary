#include <Wire.h>
#include <AccelStepper.h>
#include <LiquidCrystal_PCF8574.h>
#include "./SerialProtocol.h"
#include "./CustomStepper.h"

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
#define lsBackDrawer 14 // BACK DRAWER       A0
#define lsFrontDrawer 15 // FRONT DRAWER     A1
#define lsLeftElevator 9 // LEFT ELEVATOR    D8 8
#define lsRightElevator 9 // RIGHT ELEVATOR  D9 9

#define button 16
#define led 13

CustomStepper leftElevator(dirLeftElevator, stepLeftElevator, enableLeftElevator, lsLeftElevator, -1);
CustomStepper rightElevator(dirRightElevator, stepRightElevator, enableRightElevator, lsRightElevator, -1);
CustomStepper drawer(dirDrawer, stepDrawer, enableDrawer, lsBackDrawer, lsFrontDrawer);

//LiquidCrystal_PCF8574 lcd(0x27);

//int lcdError;

SerialProtocol protocol;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  Serial.readStringUntil('\n');

  pinMode(button, INPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  delay(50);
  digitalWrite(led, LOW);
  delay(100);
  digitalWrite(led, HIGH);
  delay(50);
  digitalWrite(led, LOW);
  
  leftElevator.init();
  rightElevator.init();
  drawer.init();

  // Wire.begin();
  // Wire.beginTransmission(0x27);
  // lcdError = Wire.endTransmission();

  //lcd.begin(16, 2);

  //Serial.println("SETUP: Ready");
}


int selectedElevator = 0;

void loop() {
//   if (digitalRead(button) == HIGH) {
//     digitalWrite(led, HIGH);
//   } else {
//     digitalWrite(led, LOW);
//   }
  leftElevator.loop();
  drawer.loop();
  rightElevator.loop();
  protocol.loop();

  if (protocol.hasCommand) {
      if (protocol.commandName == "STOP") {
        drawer.stop();
        leftElevator.stop();
        rightElevator.stop();

      } else if (protocol.commandName == "PING") {
        Serial.println("L: Pong!");
      } else if (protocol.commandName == "ID") {
        Serial.println("ID:STEPPER");
      } else if (protocol.commandName == "ACCL") {
        leftElevator.setAcceleration(protocol.commandParam1);
      } else if (protocol.commandName == "DRAWER_GO_TO_BACK") {
        
        drawer.continuous(protocol.commandParam1);

      } else if (protocol.commandName == "DRAWER_GO_TO_FRONT") {
        
        drawer.continuous(-protocol.commandParam1);

      } else if (protocol.commandName == "GET_CURRENT_POSITION") {
        
        Serial.print(leftElevator.getCurrentPosition());
        Serial.print(" - ");
        Serial.println(rightElevator.getCurrentPosition());

      } else if (protocol.commandName == "TWIN_GO_TO") {
        int speed = protocol.commandParam2;

        leftElevator.goTo(protocol.commandParam2, speed);
        rightElevator.goTo(protocol.commandParam2, speed);
        
      } else if (protocol.commandName == "ELEVATOR_GO_TO") {
        /**
         * Command ELEVATOR_GO_TO
         **/
        int speed = protocol.commandParam3;
        if (speed == 0) {
            speed = 200;
        }

        selectedElevator = protocol.commandParam1;
        if (selectedElevator == 0) {
            leftElevator.goTo(protocol.commandParam2, speed);
        } else {
            rightElevator.goTo(protocol.commandParam2, speed);
        }

        /**
         * -850 step maximum
         **/
      } else if (protocol.commandName == "ELEVATOR_SET_SPEED") {
        selectedElevator = protocol.commandParam1;
        //Serial.println("Elevator set speed: " + selectedElevator + " with speed: " + protocol.commandParam2);

        if (selectedElevator == 0) {
            leftElevator.continuous(protocol.commandParam2);
        } else {
            rightElevator.continuous(protocol.commandParam2);
        }
        
        if (protocol.commandParam2 == 0) {
            if (selectedElevator == 0) {
                leftElevator.stop();
            } else {
                rightElevator.stop();
            }
        }
      } else if (protocol.commandName == "TWIN_SET_SPEED") {
        if (protocol.commandParam1 == 0) {
          leftElevator.stop();
          rightElevator.stop();
        } else {
          leftElevator.continuous(protocol.commandParam1);
          rightElevator.continuous(protocol.commandParam1);
        }
      } else if (protocol.commandName == "CMD") {
        Serial.print("CMD: ");
        Serial.print(protocol.commandParam1);
        Serial.print("  ");
        Serial.print(protocol.commandParam2);
        Serial.print("  ");
        Serial.print(protocol.commandParam3);
        Serial.print("  ");
        Serial.println(protocol.commandParam4);
      // } else if (protocol.commandName == "LCD_BACKLIGHT") {
      //   lcd.setBacklight(protocol.commandParam1);
      // } else if (protocol.commandName == "LCD_CLEAR") {
      //   lcd.clear();
      // } else if (protocol.commandName == "LCD_FIRST") {
      //   lcd.home();
      //   lcd.print(protocol.commandParam4);
      // } else if (protocol.commandName == "LCD_SECOND") {
      //   lcd.setCursor(0, 1);
      //   lcd.print(protocol.commandParam4);
      // } else if (protocol.commandName == "LCD_EXIST") {
      //   if (lcdError == 0) {
      //       Serial.println("LCD_EXIST: FOUND");
      //   } else {
      //       Serial.println("LCD_EXIST: NOT_FOUND");
      //   }
      } else {
        Serial.println("E: invalid protocol.commandName");
      }
  }
}