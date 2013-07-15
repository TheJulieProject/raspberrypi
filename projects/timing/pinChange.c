/*
 * untitled.c
 * 
 * Copyright 2013  <pi@raspberrypi>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>

int main(int argc, char **argv)
{
	int seconds = 10;
	wiringPiSetup ();	
	pinMode(0, INPUT);
	while (1==1)
	{
		//pinMode (0, OUTPUT);
		//digitalWrite(0, 0);
		//sleep(seconds);
		//digitalWrite(0,1);
		//sleep(seconds);		
		//sleep(seconds);
		pullUpDnControl(0, PUD_DOWN);
		sleep(seconds);
		pullUpDnControl(0, PUD_UP);
		sleep(seconds);
		//pullUpDnControl(0, PUD_OFF);
		//sleep(seconds);
	} // while
	return 0;
} // main

