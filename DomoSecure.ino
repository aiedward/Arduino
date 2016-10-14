const int PIRPin = 2;
int PIRState = LOW;
const int LEDPin = 13;

void setup()
{
	  pinMode(PIRPin, INPUT);
	  pinMode(LEDPin, OUTPUT);
	  Serial.begin(115200);
    while (!Serial){
    ; // wait for serial port to connect. Needed for native USB
    }
}

void loop()
{ 	
    pirSensor();  	

    if (Serial.available())
  	    receivedData();   

    delay(1); // delay in between reads for stability
}

void pirSensor()
{
    int value = digitalRead(PIRPin);
    
    if (value == HIGH) //detect movement.
    {          
          if (PIRState == LOW)
          {  // code to make a camera shoot by python.
              Serial.write(1);
              PIRState = HIGH;
          }
     }
     else
     {
          if (PIRState == HIGH)
          {   // code to stop a camera shoot by python.
              Serial.write(0);
              PIRState = LOW;
          }
     } 
}


void receivedData()
{// data receive from the python software after analize the picture taken.
 // 0-ok, 1-ko, #?-blink.  
        char danger = Serial.read();
        
        switch (danger)
        {
            case '0': //green rect.. know faces.. todo bien. 
              digitalWrite(LEDPin, LOW); 
              delay(500);
              digitalWrite(LEDPin, HIGH);
              delay(500);
              digitalWrite(LEDPin, LOW);
              delay(500);
              digitalWrite(LEDPin, HIGH); 
              delay(500);
              digitalWrite(LEDPin, LOW);
              delay(500);
              digitalWrite(LEDPin, HIGH);
              delay(500);
              digitalWrite(LEDPin, LOW);
              delay(500);
              digitalWrite(LEDPin, HIGH); 
              delay(500);
              digitalWrite(LEDPin, LOW); 
              delay(500);
              digitalWrite(LEDPin, HIGH);
              delay(500);
              digitalWrite(LEDPin, LOW);
              delay(500);
              digitalWrite(LEDPin, HIGH); 
              delay(500);
              digitalWrite(LEDPin, LOW);
            break;
            case '1': //red rect.. unknow faces.. algo mal.
              digitalWrite(LEDPin, HIGH);
              delay(8000);
              digitalWrite(LEDPin, LOW);
            break;
            default:
              digitalWrite(LEDPin, LOW);
        }
}
