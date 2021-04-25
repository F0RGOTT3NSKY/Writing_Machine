#include <Servo.h>

Servo servo;
bool pen = false;
int resolution = 100; //resolution in ms

void pen_down(){
  servo.write(90);
}

void pen_up(){
  servo.write(0);
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

void setup() {
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  servo.attach(6);
  Serial.begin(9600);
  stop_motors();
  pen_up();
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
        if (pen){
          pen = false;
          pen_up();
        } else {
          pen = true;
          pen_down();
        }
        break;
      default:
        // do nothing
        break;
    }
  }
}
