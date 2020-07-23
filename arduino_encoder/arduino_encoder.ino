#include "./SerialProtocol.h"

int val;
int encoder0PinA = 14;
int encoder0PinB = 15;
int encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;
int encoderUntil = 0;

bool encoderEnabled = false;

SerialProtocol protocol;

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(50);
  Serial.readStringUntil('\n');

  //Serial.println("SETUP");

  pinMode(encoder0PinA, INPUT);
  pinMode(encoder0PinB, INPUT);
}

void loop()
{
  protocol.loop();
  if (protocol.hasCommand)
  {
    if (protocol.commandName == "ID")
    {
      Serial.println("ID:ENCODER");
    }
    else if (protocol.commandName == "PING")
    {
      Serial.println("L: Pong!");
    }
    else if (protocol.commandName == "ENCODER_UNTIL")
    {
      encoder0Pos = 0;
      encoderEnabled = true;
      encoderUntil = protocol.commandParam1;
    }
    else if (protocol.commandName == "ENCODER_ENABLE")
    {
      encoderEnabled = true;
    }
    else if (protocol.commandName == "ENCODER_DISABLE")
    {
      encoderEnabled = false;
    }
    else if (protocol.commandName == "ENCODER_RESET")
    {
      encoder0Pos = 0;
    }
    else
    {
      Serial.println("E: invalid commandName");
    }
  }

  if (encoderEnabled)
  {
    n = digitalRead(encoder0PinA);
    if ((encoder0PinALast == LOW) && (n == HIGH))
    {
      if (digitalRead(encoder0PinB) == LOW)
      {
        encoder0Pos--;
      }
      else
      {
        encoder0Pos++;
      }
      // Serial.print("Pos: ");
      // Serial.println(encoder0Pos);
      if ((encoderUntil > 0 && encoder0Pos >= encoderUntil) || (encoderUntil < 0 && encoder0Pos <= encoderUntil))
      {
        encoderEnabled = false;
        Serial.print("Done ");
        Serial.print(encoder0Pos);
        Serial.println(" steps");
      }
    }
    encoder0PinALast = n;
  }
}
