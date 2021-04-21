#include <Servo.h>

Servo servo;
int resolution = 100; //resolution in ms

void no_color(){
  servo.write(0);
  digitalWrite(12,LOW);
  digitalWrite(11,LOW);
  digitalWrite(13,LOW);
}

void stop_motors(){
  digitalWrite(2,LOW);
  digitalWrite(3,HIGH);
  digitalWrite(4,LOW);
  digitalWrite(5,HIGH);
}

void move_up(int ms){
  digitalWrite(3,LOW);
  delay(ms);
  stop_motors();
}

void move_down(int ms){
  digitalWrite(2,HIGH);
  delay(ms);
  stop_motors();
}

void move_left(int ms){
  digitalWrite(4,HIGH);
  delay(ms);
  stop_motors();
}

void move_right(int ms){
  digitalWrite(5,LOW);
  delay(ms);
  stop_motors();
}

void light_red(){
  servo.write(0);
  digitalWrite(11,LOW);
  digitalWrite(12,HIGH);
  digitalWrite(13,LOW);
}

void light_blue(){
  servo.write(0);
  digitalWrite(11,HIGH);
  digitalWrite(12,LOW);
  digitalWrite(13,LOW);
}

void light_green(){
  servo.write(90);
  digitalWrite(11,LOW);
  digitalWrite(12,LOW);
  digitalWrite(13,HIGH);
}

void setup() {
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  servo.attach(6);
  Serial.begin(9600);
  stop_motors();
  no_color();
}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    switch (incomingByte) {
      case 119:
        move_up(resolution);
        break;
      case 97:
        move_left(resolution);
        break;
      case 115:
        move_down(resolution);
        break;
      case 100:
        move_right(resolution);
        break;
      case 32:
        no_color();
        break;
      case 114:
        light_red();
        break; 
      case 103:
        light_green();
        break; 
      case 98:
        light_blue();
        break;
      default:
        Serial.print(incomingByte);
        break;
    }
  }
}
