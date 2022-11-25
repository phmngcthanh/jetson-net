
#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
#include "SSD1306.h" // alias for `#include "SSD1306Wire.h"`
#include <ESP8266WiFi.h>
const bool Debug = 1; // disable all serial signal if not Debug
const int trig = 15;     // We set the Trigger pin of the Ultrasound 
const int echo = 12;     // We set the Echo pin of the Ultrasound 
const int SoundSpeed=350 ;// meters per second at 30 celsius

const int RED = 4; //D2 pin
const int YELLOW = 5; //D1 pin
const int GREEN = 4;



void ControlLed(int state, int duration = 1000)// in milisecs
{
    if (state == 0) //Startup
    {//Enable all LEDs
        digitalWrite(RED,1);
        digitalWrite(YELLOW,1);
        delay(duration);
        digitalWrite(RED,0);
        digitalWrite(YELLOW,0);
        // Enable LED 1
        digitalWrite(RED,1);
        delay(duration);
        digitalWrite(RED,0);
        // Enable LED2
        digitalWrite(YELLOW,1);
        delay(duration);
        digitalWrite(YELLOW,0);
    }
    if (state == 1)
    {
        digitalWrite(YELLOW,1);
        delay(duration);
        digitalWrite(YELLOW,0);
    }
    if (state == 2)
    {
        digitalWrite(RED,1);
        delay(duration);
        digitalWrite(RED,0);
    }
}

int DoDistance()
{
    float Soundpace;
    Soundpace = 1/SoundSpeed; //seconds per meter
    Soundpace = Soundpace*(1000000/100); // convert to microseconds per centimeter
    unsigned long duration;
    int distance;
    digitalWrite(trig,0);
    delayMicroseconds(2);
    digitalWrite(trig,1);
    delayMicroseconds(5);
    digitalWrite(trig,0);
    // width of Echo pin
    duration = pulseIn(echo,HIGH);
    distance = int(duration/(2*Soundpace));
    if(Debug)
    {Serial.print(distance);
    Serial.println("cm");}
    return distance;
}
void setup() {
    Serial.begin(9600);
    pinMode(trig,OUTPUT);   //Trigger pin is OUTPUT of 8266
    pinMode(echo,INPUT);    // Meanwhile  Echo is input from Ultrasound
    pinMode(D2,OUTPUT); 
    pinMode(D1,OUTPUT);
}
void loop() {
  int x=DoDistance();
  if (x<100) {
    digitalWrite(D2,1);
    delay(1000);
    digitalWrite(D2,0);
}
 

 delay(500);

 }