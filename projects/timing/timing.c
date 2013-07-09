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
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define ST_BASE (0x20003000)
#define TIMER_OFFSET (4)

int main(int argc, char *argv[]) 
{
	long long int t, prev, *timer; // 64 bit timer
	int fd;
	void *st_base; // byte ptr to simplify offset math
	int seconds = 1; // time we want the progam to wait between intervals
	int readings_so_far = 0;
	long long int accumulated_time = 0;
	
	// get access to system core memory
	if (-1 == (fd = open("/dev/mem", O_RDONLY))) 
	{
		fprintf(stderr, "open() failed.\n");
		return 255;
	}
	
	// map a specific page into process's address space
	if (MAP_FAILED == (st_base = mmap(NULL, 4096,
						PROT_READ, MAP_SHARED, fd, ST_BASE))) 
	{
		fprintf(stderr, "mmap() failed.\n");
		return 254;
	}
	
	// set up pointer, based on mapped page
	timer = (long long int *)((char *)st_base + TIMER_OFFSET);
	
	// read initial timer
	prev = *timer;	
	
	// and wait
	sleep(seconds);
	
	while (1==1) // forever
	{ 
		// read new timer
		t = *timer;
		
		// get difference
		long long int difference = t - prev - 1000000;
		// print difference (and flush output)
		//printf("Timer = %lld    \n", t);
		printf("Timer diff = %lld \n", difference); // Don't take the second into account
		
		// keep average		
		printf("Average = %lld \n", (accumulated_time += difference) / (readings_so_far+=1));
		
		fflush(stdout);
		
		// save current timer
		prev = t;
		
		// and wait
		sleep(seconds);
	}
	// will never get here
	return 0;
}
