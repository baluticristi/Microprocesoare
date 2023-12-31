#include "MKL25Z4.h"

extern uint8_t led_state;

void PIT_Init(void); /* Functie de initializarea a modulului periferic*/
void PIT_IRQHandler(void); /* Functia de tratarea a intreruperilor pentru perifericul PIT*/
