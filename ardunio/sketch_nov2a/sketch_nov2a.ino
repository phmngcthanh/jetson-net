// Copyright (c) 2022. Thanh Pham Ngoc <phmngcthanh <AT>gmail.com>
//  All rights reserved.
//  A copy of the license can be found at the LICENSE file, or the link https://github.com/phmngcthanh/jetson-net/blob/master/LICENSE


#include "Base64.h"
#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
#include <ESP8266WiFi.h>



//// DANGER SECTION
// The following parameters affects the communication and therefore shall not be changed
const char PRIVATE_KEY[] = "1952095819520262";
char ssid[] = "The Grace";     //  your network SSID (name)
char pass[] = "99999999";  // your network password
//// END DANGER SECTION


//// DATA TYPE SECTION
//Elegant way to store bytes and convert to int, accroding to Stackoverflow
union Randombytes {
    char myByte[8];
    unsigned long long mylong;
    long myslong[2];
} ;
union Socketbytes{
    char myByte[16];
    unsigned long long mylong[2];
} ;

//// END DATA TYPE SECTION

//# Packet:
//# 1.  for Confidental, Integrity and Authentication purpose)
//# 1.1
//# 2.
//# Packet include 16 bytes
//# To avoid cryptanalyst from using same private key, we use a random IV and xor with the payload. Then we XOR them all with private key
//# |IV ( 8 bytes random)| Type of Packet (1 bytes)| ID of sent packet device (essp8266) (1bytes - 254 devices, server ID =0)|
//# | content (5 bytes) | checksum ( exclude the IV, by XORed them byte-by-byte)|
//#type of Packet: 1: Request Auth; 2: ResponseAuth
//#Content: x means different than 0
//#[x][ ][ ][ ][ ]: From the Client Ultrasound
//#[ ][x][x][ ][ ]: From the Client other devices(NFC...)
//#[ ][ ][ ][x][ ]: From the Server accept
//#[ ][ ][ ][ ][x]: from the Server reject

//// DECLARE SECTION
const int DeviceSerial=1;
const int trig = 15;     // We set the Trigger pin of the Ultrasound
const int echo = 12;     // We set the Echo pin of the Ultrasound
const int SoundSpeed=340 ;// meters per second
const bool Debug = 1;
int status = WL_IDLE_STATUS;     // the Wifi radio's status
IPAddress server(192,168,0,166);
const int port = 19520;
WiFiClient client;
Socketbytes privkey;

//// END DECLARE SECTION
int getXOR(int x, int y) {
    return (x | y) & (~x | ~y);
}
unsigned long long  getXOR(unsigned long long x, unsigned long long y) {
    return (x | y) & (~x | ~y);
}
bool is_big_endian(void)
{
    union {
        uint32_t i;
        char c[4];
    } bint = {0x01020304};

    return bint.c[0] == 1;
}
// we apply secure random  https://github.com/esp8266/Arduino/pull/2142 to generate CSRNG
Socketbytes GenRandom(){
    Socketbytes Return;
    for (int i=0;i<8;i++)
        Return.myByte[i]=secureRandom(255);

    return Return;
}


void setup() {
    if (Debug)
        Serial.setDebugOutput(true);
    Serial.begin(9600);     // giao tiếp Serial với baudrate 9600
    pinMode(trig,OUTPUT);   //Trigger pin is OUTPUT of 8266
    pinMode(echo,INPUT);    // Meanwhile  Echo is input from Ultrasound
    pinMode(D2,OUTPUT);
    pinMode(D1,OUTPUT);
    ControlLed(0,1000);
    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to  SSID: ");
        Serial.println(ssid);
        //status = WiFi.begin(ssid);
        status = WiFi.begin(ssid, pass);
        delay(10000);
    }
    if (Debug)
    {
       WiFi.printDiag(Serial);}
        for (int i=0;i<16;i++)
        {
          privkey.myByte[i]=PRIVATE_KEY[i];
        }
        /*
        privkey.mylong[0]=4050206319053191473;
        privkey.mylong[1]=3618134533220940081;*/
}
int DoDistance(){
    if (Debug)
        return 10;
    unsigned long duration;
    int distance;
    digitalWrite(trig,0);
    delayMicroseconds(2);
    digitalWrite(trig,1);
    delayMicroseconds(5);
    digitalWrite(trig,0);
    duration = pulseIn(echo,HIGH);
    distance = int(duration/2/29.412);
    Serial.print(distance);
    Serial.println("cm");
    return distance;
}
int ControlLed(int state, int duration){
    if (state == 0) //Startup
    {//Enable all leds
        digitalWrite(D2,1);
        digitalWrite(D1,1);
        delay(duration);
        digitalWrite(D2,0);
        digitalWrite(D1,0);
        // Enable LED 2
        digitalWrite(D2,1);
        delay(duration);
        digitalWrite(D2,0);
        // Enable LED1
        digitalWrite(D1,1);
        delay(duration);
        digitalWrite(D1,0);
    }
        if (state == 1) //yes
    {//Enable all leds
        digitalWrite(D2,0);
        digitalWrite(D1,0);
        // Enable LED1
        digitalWrite(D1,1);
        delay(duration);
        digitalWrite(D1,0);
    }
            if (state == 2) //no
    {//Enable all leds
        digitalWrite(D2,0);
        digitalWrite(D1,0);
        // Enable LED1
        digitalWrite(D2,1);
        delay(duration);
        digitalWrite(D2,0);
    }
    return 0;

}
Socketbytes BuildSB(int& nonce,int status=1) {
  //provide information
  Socketbytes tmp = GenRandom();
  tmp.mylong[1]=0;//clear
  tmp.myByte[8]=status;// RequestAuth
  tmp.myByte[9]=DeviceSerial;
  tmp.myByte[10]= secureRandom(256);
  nonce =tmp.myByte[10];
  tmp.myByte[15] =getXOR(tmp.myByte[8],tmp.myByte[9]);
  tmp.myByte[15]=  getXOR(tmp.myByte[10],tmp.myByte[15]);
  //doing XORing
  tmp.mylong[1]=getXOR(tmp.mylong[1],tmp.mylong[0]);
  //encryption
  Serial.println(privkey.mylong[1]);
  tmp.mylong[0]=getXOR(tmp.mylong[0],privkey.mylong[0]);
  tmp.mylong[1]=getXOR(tmp.mylong[1],privkey.mylong[1]);
  return tmp;
}
int Authen(Socketbytes recv, int nonce){ //Recv response from server
  Socketbytes tmp=recv;
  //0 means no 1 means yes
  tmp.mylong[0]=getXOR(tmp.mylong[0],privkey.mylong[0]);
  tmp.mylong[1]=getXOR(tmp.mylong[1],privkey.mylong[1]);
  tmp.mylong[1]=getXOR(tmp.mylong[1],tmp.mylong[0]);
  for (int i=0;i<16;i++)
  {Serial.print((int)tmp.myByte[i]);
  Serial.print("-");}
  if ((int)tmp.myByte[8]!=2)
    Serial.print("Wrong AuthRes ");
    return 0;
  if ((int)tmp.myByte[9]!=0)
    Serial.print("Wrong device");
    return 0;
  if ((int)tmp.myByte[15]!=nonce)
    Serial.print("Wrong nonce");
    return 0;
  for (int i = 0; i<5; i++)
    if ((int)tmp.myByte[10+i]!=1){
      Serial.print("pottential bitflip");
      return 0;
    }
  Serial.print("succ!");
  return 1;
}
void loop() {
  int x=DoDistance();
  if (x<50) {
  for (int i=0; i<10;i++){
  ControlLed(2,100);
  delay(100);}


  if (client.connect(server, port)) {
    Serial.println("connected to server");
    int nonce;
    Socketbytes bytecode=BuildSB(nonce,1);
    Socketbytes recvbytes;
    int enclen=base64_enc_len(16);
    char encoded[enclen];
    char decoded[enclen];
    base64_encode(encoded, bytecode.myByte, 16);
    client.flush();
    client.println(encoded);

    client.setTimeout(5000); // default is 1000
    Serial.println("recv:");
    for (int i=0;i<24;i++)
    {
      if (client.connected())
      if (client.available())
      encoded[i]=client.read();
      else {Serial.print("not avail????");Serial.println(i);
      delay(5000);}
    }
    base64_decode(decoded,encoded,24);
    for (int i=0;i<16;i++)
      recvbytes.myByte[i]=decoded[i];
    Serial.println(decoded);
    if(Authen(recvbytes, nonce))
      for (int i=0;i<10;i++)
      ControlLed(1,500);
    else
      for (int i=0;i<10;i++)
        ControlLed(2,500);
    if (Debug)
      delay(5000);
    else
      delay (1000);
  }}
  else delay(500);
}