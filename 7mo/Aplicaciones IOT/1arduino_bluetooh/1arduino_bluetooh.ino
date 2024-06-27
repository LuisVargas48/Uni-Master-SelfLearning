 #include <Servo.h>
Servo servo;

char entrada;

void setup() {
servo.attach(2);
 Serial.begin(9600);
}

void loop() {
if(Serial.available()){
    entrada=Serial.read();
     servo.write(360);
}else{if (entrada=='E'){
  servo.write(90);
  }
  
  }
}
