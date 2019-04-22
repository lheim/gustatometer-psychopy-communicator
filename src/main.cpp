#include <Arduino.h>

int triggered = 0;
int counter = 0;
float voltageLevel = -1;
String command;

unsigned long StartTime = 0;
unsigned long StopTime = 0;
unsigned long ElapsedTime = 0;
unsigned long ReactionTime = 0;


void setup() {
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(D0, LOW);
  digitalWrite(D1, LOW);

  StartTime = millis();

  Serial.begin(115200);
  Serial.println("Setup finished.");
}

void loop() {
  if(Serial.available() > 3)
  {
    command = Serial.readStringUntil('\n');
    Serial.print("Received Command: ");
    Serial.println(command);
    if(command == "START")
    {
      digitalWrite(D0, HIGH);
      counter = 0;
      Serial.println("Starting Paradigma ... ");
    }
    else if(command == "STOP") //unused command - there's no way to stop the gustatometer
    {
      digitalWrite(D0, LOW);
      Serial.println("Setting output voltage level to 0V.");
    }
    else
    {
      Serial.println("Unknown Command!");
    }
  }

  voltageLevel = analogRead(A0);
  voltageLevel = ((voltageLevel/1024.0)*3.3)*(5.3/2.0);   // Voltage Divider: 3.3k Ohm + 2k Ohm

  if(voltageLevel > 3 && triggered != 1) // new triggered detected
  {
    triggered = 1;
    StartTime = millis();
    digitalWrite(D1, HIGH);

    Serial.println();
    Serial.println("+++");
    Serial.println("Triggered!");
    Serial.print("No. ");
    Serial.println(counter);
    Serial.print("Voltage: ");
    Serial.print(voltageLevel);
    Serial.println("V");
    counter++;
  }
  else if (voltageLevel < 0.5 && triggered == 1) // voltage level dropped - triggered has ended
  {
    StopTime = millis();
    ElapsedTime = StopTime - StartTime;
    if(ElapsedTime > 10)
    {
      triggered = 0;
      digitalWrite(D1, LOW);
      Serial.println("---");
      Serial.println("Trigger stopped!");
      Serial.print("Time: ");
      Serial.print(ElapsedTime);
      Serial.println("ms");
    }
  }
}
