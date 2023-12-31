#include "Adc.h"
#include "Uart.h"
#include "gpio.h"
#include "Pit.h"
#include "Adc.h"


int main() {
	
	RGBLed_Init();
	UART0_Init(9600);
	PIT_Init();
	ADC0_Init();
	

	
	for(;;){ 
		
		int count=10000;
		while(count)
		{
			count--;
		}
			uint16_t measured_voltage =ADC0_Read();
		
			
		if (measured_voltage <= 10000) {
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOC_PCOR |= (1 << Bread_BLUE_LED_PIN);
						GPIOA_PCOR |= (1 << Bread_YELLOW_LED_PIN);
		} else if (measured_voltage < 40000) {
			
						GPIOA_PSOR |= (1 << Bread_YELLOW_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOC_PCOR |= (1 << Bread_BLUE_LED_PIN);
				} else{
						GPIOC_PSOR |= (1 << Bread_BLUE_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_YELLOW_LED_PIN);
				}

			
			uint8_t parte_zecimala=(measured_voltage/10000)%10;
			uint8_t parte_fractionara1=(measured_voltage /1000) % 10;
			uint8_t parte_fractionara2=(measured_voltage /100) % 10;
			uint8_t parte_fractionara3 = (measured_voltage /10) % 10;
			uint8_t parte_fractionara4 = (measured_voltage) % 10;
		


			UART0_Transmit('V');
			UART0_Transmit('a');
			UART0_Transmit('l');
			UART0_Transmit('u');
			UART0_Transmit('e');
			UART0_Transmit(' ');
			UART0_Transmit('=');
			UART0_Transmit(' ');
			UART0_Transmit(parte_zecimala + 0x30);
			UART0_Transmit(parte_fractionara1 + 0x30);
			UART0_Transmit(parte_fractionara2 + 0x30);
			UART0_Transmit(parte_fractionara3 + 0x30);
			UART0_Transmit(parte_fractionara4 + 0x30);
			UART0_Transmit(0x0A);
			UART0_Transmit(0x0D);
	}
	
}
