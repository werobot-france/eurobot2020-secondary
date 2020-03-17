int val;
int encoder0PinA = 14;
int encoder0PinB = 15;
int encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;

String command = "";
String commandName = "";
bool encoderEnabled = false;

void setup()
{
    Serial.begin(9600);
    Serial.setTimeout(50);
    //Serial.println("SETUP");

    pinMode(encoder0PinA, INPUT);
    pinMode(encoder0PinB, INPUT);
}

void loop()
{
    if (Serial.available())
    {
        command = Serial.readStringUntil('\n');
        if (command != "")
        {
            commandName = command;
            if (commandName == "ID")
            {
                Serial.println("ID:ENCODER");
            }
            else if (commandName == "PING")
            {
                Serial.println("L: Pong!");
            }
            else if (commandName == "ENCODER_ENABLE")
            {
                encoderEnabled = true;
            }
            else if (commandName == "ENCODER_DISABLE")
            {
                encoderEnabled = false;
            }
            else if (commandName == "ENCODER_RESET")
            {
                encoder0Pos = 0;
            }
            else
            {
                Serial.println("E: invalid commandName");
            }
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
            Serial.print("Pos: ");
            Serial.println(encoder0Pos);
        }
        encoder0PinALast = n;
    }
}
