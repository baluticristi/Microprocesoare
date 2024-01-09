#include "Adc.h"
#include "Uart.h"
#include "gpio.h"
#include "Pit.h"
#include "Adc.h"


int main() {
	
	RGBLed_Init();
	PIT_Init();
	ADC0_Init();
	UART0_Init(9600);

	
	for(;;){ 
		
			uint16_t measured_sound =ADC0_Read();
	
		int switcher=0;
		if (measured_sound <= 250&&switcher==0) {
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOC_PCOR |= (1 << Bread_BLUE_LED_PIN);
						GPIOA_PCOR |= (1 << Bread_YELLOW_LED_PIN);
		}
		else if (measured_sound < 1250&&switcher==0) {
						GPIOA_PSOR |= (1 << Bread_YELLOW_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOC_PCOR |= (1 << Bread_BLUE_LED_PIN);
				}
		else if(measured_sound > 1250&&switcher==0){
						GPIOC_PSOR |= (1 << Bread_BLUE_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_RED_LED_PIN);
						GPIOA_PSOR |= (1 << Bread_YELLOW_LED_PIN);
				}

			
				

	
			{
				if (measured_sound>1000){
					uint8_t cifra1=(measured_sound /1000) % 10;
					UART0_Transmit(cifra1 + 0x30);
				}
				else{
					UART0_Transmit(0x30);
				}
				
				if (measured_sound>100){
				uint8_t cifra2=(measured_sound /100) % 10;
					UART0_Transmit(cifra2 + 0x30);
				}
				else{
					UART0_Transmit(0x30);
				}
				
				if (measured_sound>10){
					uint8_t cifra3=(measured_sound /10) % 10;
					UART0_Transmit(cifra3 + 0x30);
				}
				else{
					UART0_Transmit(0x30);
				}
				
				if (measured_sound>0){
					uint8_t cifra4 = (measured_sound) % 10;
					UART0_Transmit(cifra4 + 0x30);
				}
				else{
					UART0_Transmit(0x30);
				}
				
			
				UART0_Transmit(0x0D);
				UART0_Transmit(0x0A);
			}
		


		
			
				

	}
	
}
