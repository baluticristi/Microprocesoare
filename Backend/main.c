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
		
			uint16_t measured_sound =ADC0_Read();
	
		
		if (measured_sound <= 250) {
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOC_PCOR |= (1 << Bread_BLUE_LED_PIN);
						GPIOA_PCOR |= (1 << Bread_YELLOW_LED_PIN);
		}
		else if (measured_sound < 1250) {
						GPIOA_PSOR |= (1 << Bread_YELLOW_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOC_PCOR |= (1 << Bread_BLUE_LED_PIN);
				}
		else if(measured_sound > 1250){
						GPIOC_PSOR |= (1 << Bread_BLUE_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_YELLOW_LED_PIN);
				}

			
				
			if(measured_sound>15)
	
			{uint8_t cifra1=(measured_sound /1000) % 10;
			uint8_t cifra2=(measured_sound /100) % 10;
			uint8_t cifra3 = (measured_sound /10) % 10;
			uint8_t cifra4 = (measured_sound) % 10;
		


		
			UART0_Transmit(cifra1 + 0x30);
			UART0_Transmit(cifra2 + 0x30);
			UART0_Transmit(cifra3 + 0x30);
			UART0_Transmit(cifra4 + 0x30);
			
			UART0_Transmit(0x0D);
			UART0_Transmit(0x0A);}
			else{
			
			


		
			UART0_Transmit(0x30);
			UART0_Transmit(0x30);
			UART0_Transmit(0x30);
			UART0_Transmit(0x30);
			
			UART0_Transmit(0x0D);
			UART0_Transmit(0x0A);
			
			}
		
			
				

	}
	
}
