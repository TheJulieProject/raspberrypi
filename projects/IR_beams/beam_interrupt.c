
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

// Globals
int detections = 0;


// Function to be executed by the ISR when a RISING interrupt
// occurs on the IR_Receiver_pin
void beamBrokenInterrupt()
{
  detections++;
  printf("detected #%d\n", detections);
  
  // A delay of 150ms helps to 'debounce' the beam
  delay(150);
} // beamBrokenInterrupt


// Infrared beam break detection
// using IR LED and IR receiver
int main(int argc, char* argv[])
{
  printf("*************\n");
  printf("Infrared beam breaking with interrupts\n");
  printf("*************\n");

  int IR_LED_pin = 7, IR_Receiver_pin = 1;
  int limit = atoi(argv[1]);
  
  // Setup wiring Pi GPIO pins.
  // NOTE: pins are numbered by WiringPi convention!
  wiringPiSetup();

  // Set wiringPi GPIO 7 (BCM GPIO 4) to be a general purpose clock
  // and wiringPi GPIO 1 (BCM GPIO 18) to be an input
  pinMode(IR_LED_pin, GPIO_CLOCK);
  pinMode(IR_Receiver_pin, INPUT);
  // Set the clock frequency at 38kHz so the IR receiver picks up the LED
  digitalWrite(IR_LED_pin, 38000);

  // Register the IR receiver to interrupt when the beam
  // is broken and execute my ISR
  wiringPiISR(IR_Receiver_pin, INT_EDGE_RISING, &beamBrokenInterrupt);
  
  // Detect X amount of times and then prepare to exit
  while (detections != limit)
  {}

  // Deinitialise used pins (GPIO are set to be INPUT by default)
  pinMode(IR_LED_pin, INPUT);
  
  // Program exists cleanly
  return 0;
} // main
