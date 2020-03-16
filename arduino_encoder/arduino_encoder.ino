int val;
int encoder0PinA = 14;
int encoder0PinB = 15;
int encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;

void setup() {
  pinMode(encoder0PinA, INPUT);
  pinMode(encoder0PinB, INPUT);

  Serial.begin(9600);
  Serial.setTimeout(50);
}

String command = "";
String commandName = "";

void loop() {
  if (Serial.available()) {
      command = Serial.readStringUntil('\n');
      if (command != "") {
         commandName = command.substring(0, command.indexOf("#"));
         if (commandName == "ID") {
             Serial.println("ID:ENCODER");
         }
         if (commandName == "PING") {
             Serial.println("PONG!");
         }
      }
  }
  n = digitalRead(encoder0PinA);
  if ((encoder0PinALast == LOW) && (n == HIGH)) {
    if (digitalRead(encoder0PinB) == LOW) {
      encoder0Pos--;
    } else {
      encoder0Pos++;
    }
    Serial.print("Pos: ");
    Serial.println(encoder0Pos);
  }
  encoder0PinALast = n;
}

