
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include <poll.h>
#include <pthread.h>
#include <sched.h>

#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


/* Reference: BCM2835 ARM Peripherals, page 172 */
#define SYSTEM_TIMER_BASE      (0x20003000)   /* system timer address */

/* The following are OFFSETS to be used with the system timer base address */
#define SYSTEM_TIMER_CONTROL_STATUS   (0x0)   /* timer control/status */
#define SYSTEM_TIMER_CLO              (0x4)   /* timer lower 32 bits */
#define SYSTEM_TIMER_CHI              (0X8)   /* timer higher 32 bits */
#define SYSTEM_TIMER_C0               (0xC)   /* timer compare register 0 */
#define SYSTEM_TIMER_C1               (0x10)  /* timer compare register 1 */
#define SYSTEM_TIMER_C2               (0x14)  /* timer compare register 2 */
#define SYSTEM_TIMER_C3               (0x18)  /* timer compare register 3 */


#define BLOCK_SIZE (4*1024)


/*
 * Globals
 *********************************************************************************
 */

/*  */
static volatile uint32_t *timer;          /*  */
static volatile uint32_t *timerControl;   /*  */
static volatile uint32_t *timerCompare;   /*  */

unsigned long previousTime, ticks = 0;    /*  */

/*  */
unsigned long interruptFrequency;

/*  */
static void (*isrFunctions[64])(void);
int numberOfISRFunctions = 0;


/*
 * Attempt to set a high priority schedulling for the running program
 *********************************************************************************
 */
int piHiPri (int priority)
{
  struct sched_param scheduler;

  memset(&scheduler, 0, sizeof(scheduler));

  if (priority > sched_get_priority_max(SCHED_RR))
    scheduler.sched_priority = sched_get_priority_max(SCHED_RR);
  else
    scheduler.sched_priority = priority;

  return sched_setscheduler(0, SCHED_RR, &scheduler);
}


/*
 *
 *********************************************************************************
 */
void setTimerInterruptFrequency (long long int frequency)
{
  int fd;                   // file descriptor to be used for /dev/mem
  void *system_timer_base;  // byte ptr to simplify offset math
  
  //piHiPri(100);

  // get access to system core memory
  if ((fd = open("/dev/mem", O_RDWR)) == -1) 
  {
    fprintf(stderr, "open() failed.\n");
    exit(255);
  }
  
  // map a specific page into process's address space
  system_timer_base = mmap(0, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, SYSTEM_TIMER_BASE);
  if (system_timer_base == -1) 
  {
    fprintf(stderr, "mmap() failed.\n");
    exit(254);
  }
  
  // set up pointer, based on mapped page
  timer        = (uint32_t *)((char *)system_timer_base + SYSTEM_TIMER_CLO);
  timerControl = (uint32_t *)((char *)system_timer_base + SYSTEM_TIMER_CONTROL_STATUS);
  timerCompare = (uint32_t *)((char *)system_timer_base + SYSTEM_TIMER_C1);
  
  interruptFrequency = frequency;
}


/*
 *
 *********************************************************************************
 */
int waitForTimerInterrupt (int mS)
{
  int x, fd;
  char c;
  struct pollfd polls;

// Setup poll structure

  polls.fd     = *timerCompare;
  polls.events = POLLPRI; // Urgent data!

// Wait for it ...

  x = poll(&polls, 1, mS);

// Do a dummy read to clear the interrupt
//  A one character read appars to be enough.

  (void)read(*timerCompare, &c, 1);

  printf("Poll ended with x = %d", x);
  return x;
}


/*
 * 
 *********************************************************************************
 */
static void *interruptHandler (void *arg)
{
  piHiPri(100);  // Only effective if we run as root

  for (;;)
    if (waitForTimerInterrupt(-1) > 0)
    {
      for (int index = 0; index < numberOfISRFunctions; index++)
        isrFunctions[index]();

      *timerCompare = *timer + interruptFrequency;

      printf("CS before: %zu\n", *timerControl);
      *timerControl &= 0xFD;
      printf("CS after:  %zu\n", *timerControl);
    }

  return NULL;
}


/*
 *
 *********************************************************************************
 */
void registerTimerISR (void (*function)(void))
{
  pthread_t threadId;

  isrFunctions[numberOfISRFunctions++] = function;

  printf("CS before: %zu\n", *timerControl);
  *timerControl &= 0xFF;
  printf("CS after:  %zu\n", *timerControl);


  printf("CMP before: %zu\n", *timerCompare);
  *timerCompare = *timer + interruptFrequency;
  printf("CMP after:  %zu\n", *timerCompare);
  
  pthread_create(&threadId, NULL, interruptHandler, NULL);
  
  /*
  pthread_mutex_lock (&pinMutex) ;
    pinPass = pin ;
    while (pinPass != -1)
      delay (1) ;
  pthread_mutex_unlock (&pinMutex) ;
  */  
}


/*
 * 
 *********************************************************************************
 */
void printTimer ()
{
  printf("interrupt occured - timer value is: %zu @ %lu ticks\n", *timer, ++ticks);
}


/*
 * 
 *********************************************************************************
 */
void timerInterval ()
{
  if (previousTime != 0)
    printf("interrupt interval: %zu", (uint32_t)(*timer - previousTime));

  previousTime = *timer;
}


/*
 * 
 *********************************************************************************
 */
int main(int argc, char* argv[])
{
  setTimerInterruptFrequency(10000000);  
  

  registerTimerISR(&printTimer);
  //registerTimerISR(&timerInterval);

  while (1) ;

  /* Program exits cleanly. */
  return 0;
}
