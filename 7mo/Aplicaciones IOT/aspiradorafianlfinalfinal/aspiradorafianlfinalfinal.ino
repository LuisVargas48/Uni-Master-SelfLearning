#include <Servo.h>
Servo servoLlanta;
Servo servoVel;
char entrada;
const int Trigger = 5;
const int TriggerD=8;
const int TriggerI=11; 

const int Echo = 4; 
const int EchoD=7;
const int EchoI=10;

int LedR=3;
int LedD=6 ;
int LedI=9;


void setup() {
  servoVel.attach(12);
  
servoLlanta.attach(2);
  
  Serial.begin(9600);
  pinMode(Trigger, OUTPUT); 
  pinMode(Echo, INPUT);  
  digitalWrite(Trigger, LOW);
  
  pinMode(TriggerD, OUTPUT); 
  pinMode(EchoD, INPUT); 
  digitalWrite(TriggerD, LOW);
  
  pinMode(TriggerI, OUTPUT); 
  pinMode(EchoI, INPUT);  
  digitalWrite(TriggerI, LOW);
  servoLlanta.write(100);
  servoVel.write(90);
}


void loop(){




 
if(Serial.available()){
    entrada=Serial.read();
  switch(entrada){
     case 'A':
     do{sensorF();}while(entrada=='A');
     
     break;
     case 'E':
     servoVel.write(90);
     servoLlanta.write(80);
     break;

}}
}
 
  
  
  


  
const void  sensorF()
{
  bool apagado=false;

  long t; //timepo que demora en llegar el eco
  long d; //distancia en centimetros
  long dD;
  long dI;
  servoVel.write(180);
  servoLlanta.write(90);
do{
  

  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);
  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = t/59;    //escalamos el tiempo a una distancia en cm
dD=sensorD();
dI=sensorI();
Serial.print("d: ");
Serial.print(d);
Serial.println("\n");



 
  if(d<30){
if(dD>dI){
  
  servoVel.write(0);
   servoLlanta.write(45);
   delay(3000);}
    else {
      
        servoVel.write(0);
      servoLlanta.write(135);
   delay(3000);
  }

  }
    else {
     
      servoVel.write(180);
      servoLlanta.write(85);
       
 }
 }while(apagado==true);
 
if(Serial.available()){
    entrada=Serial.read();
  switch(entrada){
     case 'A':
     sensorF();
     
     break;
     case 'E':
     servoVel.write(90);
     servoLlanta.write(90);
     break;
  }}
}

int sensorD()
{
  bool down=false;

  long t; //timepo que demora en llegar el eco
  long d; //distancia en centimetros
do{
  
  digitalWrite(TriggerD, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(TriggerD, LOW);
  t = pulseIn(EchoD, HIGH); //obtenemos el ancho del pulso
  d = t/59;    //escalamos el tiempo a una distancia en cm

Serial.print("d: ");
Serial.print(d);
Serial.println("\n");
 /* if(d<10){
    digitalWrite(LedD,HIGH);
  }
    else {
         digitalWrite(LedD,LOW);
       
 }*/ 
 }while(down==true);

return d;
}



int sensorI()
{
  bool down=false;

  long t; //timepo que demora en llegar el eco
  long d; //distancia en centimetros
do{
  
  digitalWrite(TriggerI, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(TriggerI, LOW);
  t = pulseIn(EchoI, HIGH); //obtenemos el ancho del pulso
  d = t/59;    //escalamos el tiempo a una distancia en cm

Serial.print("d: ");
Serial.print(d);
Serial.println("\n");
  /*if(d<10){
    digitalWrite(LedI,HIGH);
  }
    else {
         digitalWrite(LedI,LOW);
       
 }*/
 }while(down==true);
return d;
}
