#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <AccelStepper.h>
#include <LiquidCrystal_PCF8574.h>
#include "./CustomStepper.h"

/**
 * Command interface
 **/
String command = "";
String commandName = "";
int commandParam1 = 0;
int commandParam2 = 0;
int commandParam3 = 0;
String commandParam4 = "";

int lcdError;

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

#define button 16
#define led 13

CustomStepper leftElevator(dirLeftElevator, stepLeftElevator, enableLeftElevator, lsLeftElevator, -1);
CustomStepper rightElevator(dirRightElevator, stepRightElevator, enableRightElevator, lsRightElevator, -1);
CustomStepper drawer(dirDrawer, stepDrawer, enableDrawer, lsBackDrawer, lsFrontDrawer);

LiquidCrystal_PCF8574 lcd(0x27);


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

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

  Wire.begin();
  Wire.beginTransmission(0x27);
  lcdError = Wire.endTransmission();

  lcd.begin(16, 2);

  //Serial.println("SETUP: Ready");
}


int selectedElevator = 0;

void loop() {
  if (digitalRead(button) == HIGH) {
    digitalWrite(led, HIGH);
  } else {
    digitalWrite(led, LOW);
  }
  drawer.loop();
  leftElevator.loop();

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
                commandParam4 = raw3.substring(raw3.indexOf("#") + 1, raw3.length());// last param is string
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
      if (commandName == "STOP") {
        drawer.stop();
        leftElevator.stop();
        rightElevator.stop();

      } else if (commandName == "PING") {
        Serial.println("L: Pong!");
      } else if (commandName == "DRAWER_GO_TO_BACK") {
        
        drawer.continuous(commandParam1);

      } else if (commandName == "DRAWER_GO_TO_FRONT") {
        
        drawer.continuous(-commandParam1);

      } else if (commandName == "ELEVATOR_GO_TO") {
        /**
         * Command ELEVATOR_GO_TO
         **/

        /**
         * -850 step maximum
         **/
      } else if (commandName == "ELEVATOR_SET_SPEED") {
        selectedElevator = commandParam1;
        if (commandParam2 == 0) {
            if (selectedElevator == 0) {
                leftElevator.stop();
            } else {
                rightElevator.stop();
            }
        }
        if (selectedElevator == 0) {
            leftElevator.continuous(commandParam2);
        } else {
            rightElevator.continuous(commandParam2);
        }
      } else if (commandName == "CMD") {
        Serial.print("CMD: ");
        Serial.print(commandParam1);
        Serial.print("  ");
        Serial.print(commandParam2);
        Serial.print("  ");
        Serial.print(commandParam3);
        Serial.print("  ");
        Serial.println(commandParam4);
      } else if (commandName == "LCD_BACKLIGHT") {
        lcd.setBacklight(commandParam1);
      } else if (commandName == "LCD_CLEAR") {
        lcd.clear();
      } else if (commandName == "LCD_FIRST") {
        lcd.home();
        lcd.print(commandParam4);
      } else if (commandName == "LCD_SECOND") {
        lcd.setCursor(0, 1);
        lcd.print(commandParam4);
      } else if (commandName == "LCD_EXIST") {
        if (lcdError == 0) {
            Serial.println("LCD_EXIST: FOUND");
        } else {
            Serial.println("LCD_EXIST: NOT_FOUND");
        }
      } else {
        Serial.println("E: invalid commandName");
      }
      commandParam1 = 0;
      commandParam2 = 0;
      commandParam3 = 0;
      commandParam4 = "";
    }
  }
}