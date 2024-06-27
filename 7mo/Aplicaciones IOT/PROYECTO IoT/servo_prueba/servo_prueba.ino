#include <Servo.h>

Servo servo;
void setup() {
  servo.attach(2);


}

void loop() {
   servo.write(180);
}
