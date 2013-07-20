
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>


// Infrared beam break detection
// using IR LED and IR receiver
int main(int argc, char* argv[])
{
  printf("*************\n");
  printf("Infrared beam breaking with polling\n");
  printf("*************\n");

  int IR_LED_pin = 7, IR_Receiver_pin = 1;
  int limit = atoi(argv[1]);

  wiringPiSetup();

  // Set wiringPi GPIO 7 (BCM GPIO 4) to be a general purpose clock
  // and wiringPi GPIO 1 (BCM GPIO 18) to be an input
  pinMode(IR_LED_pin, GPIO_CLOCK);
  pinMode(IR_Receiver_pin, INPUT);
  // Set the clock frequency at 38kHz so the IR receiver picks up the LED
  digitalWrite(IR_LED_pin, 38000);


  int beamBroke, previouslyBroke = 0, detections = 0;

  while (detections != limit)
  {
    beamBroke = digitalRead(IR_Receiver_pin);

    if (beamBroke)
    {
      if (!previouslyBroke)
      {        
        previouslyBroke = 1;
        detections++;
        printf("detected #%d\n", detections);        
      } // if
    } // if
    else
      previouslyBroke = 0;
    
    // Set polling rate to be 10ms 
    delay(10);
  } // for

  pinMode(IR_LED_pin, INPUT);

  // Program exists cleanly
  return 0;
} // main
