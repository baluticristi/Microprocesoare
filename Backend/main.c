#include "Adc.h"
#include "Uart.h"
#include "ClockSettings.h"
#include "gpio.h"
#include "Pit.h"


extern char c;
extern char buffer[32];

extern int write, read;
extern int print_buffer;
extern int full;

int main() {
	
	RGBLed_Init();
	UART0_Init(9600);
	PIT_Init();

	
	for(;;){ 
		
		if (read != write)	
		{
	
			if (buffer[read] == 0x0D)
			{
				//pt enter
				UART0_Transmit(0x0D); //Carriage Return
				UART0_Transmit(0x0A); //Line Feed
			}
			else 
				UART0_Transmit(buffer[read]);
			
			read++;
			read = read % 32;
		}
	}
	
}
