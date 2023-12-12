#include "Adc.h"
#include "Uart.h"
#include "ClockSettings.h"

extern uint16_t temperature_read;

int main() {
	SystemClock_Configure();
	SystemClockTick_Configure();
	UART0_Init(9600);
	ADC0_Init();
	
	for(;;){ 
		if(flag_50ms) {
			Temperature_Read();
			flag_50ms = 0U;
		}
	}
	
}
