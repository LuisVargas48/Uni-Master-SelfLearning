#include <Servo.h>
 Servo servovel;

void setup() {
servovel.attach(3);
}

void loop() {
servovel.write(180);

}
