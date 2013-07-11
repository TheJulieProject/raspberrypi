/*
 * gpio.c
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
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

//#define ST_BASE (0x7E200000)
#define ST_BASE 0x20200000

// convert decimal number to binary
void getBin(int value, int bitsCount, char* output)
{
	int i;
	output[bitsCount] = '\0';
	for (i = bitsCount - 1; i >=0; --i, value>>=1)
	{
		output[i] = (value & 1) + '0';
	}
} // getBin

int main(int argc, char *argv[]) 
{
	unsigned int t, *peripheral; // 32 bit gpio
	int fd;
	void *st_base; // byte ptr to simplify offset math
	int seconds = 2; // time we want the progam to wait between intervals
	int offset = atoi(argv[1]);
	char binary[33];
	unsigned int i, j;
	
	//printf("%d", offset);
		
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
	peripheral = (long int *)((char *)st_base);	
	printf("TEST %08X %08X\n",st_base, peripheral);
	printf("%d\n", sizeof(unsigned int));
	fflush(stdout);
		
//	while (1==1) // forever
	{ 
		// read new value
		t = peripheral[offset];
		
		// convert number to binary	
//		getBin(t, 32, binary);	
	
		// print values
//		printf("Decimal = %ld \n", t);	
		//printf("Binary = %s \n", binary); 		
	for (j = 0; j < 8; j++)
		{
		printf("\n%08X", peripheral);
		for (i = 0; i < 32; i = i + 4) printf(" %08X", peripheral[i/4]);
		peripheral += i/4;
		}
//		printf("Hex = %8X \n", t); 
//		printf("\n"); 		
		fflush(stdout);
		
		// wait
//		sleep(seconds);
	}
	printf("\n");

	// will never get here
	return 0;
} // main
