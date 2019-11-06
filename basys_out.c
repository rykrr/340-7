
/*
 * main.c
 *
 *  Created on: Aug 23, 2019
 *      Author: dave
 */
//AXI GPIO driver
#include "xgpio.h"
#include "sleep.h"
//send data over UART
#include "xil_printf.h"

//information about AXI peripherals
#include "xparameters.h"
//#include "platform.h"
#include "xsysmon.h"
#define RX_BUFFER_SIZE 4 // defines how many XADC channels are read
#define xadc XPAR_SYSMON_0_DEVICE_ID
XSysMon xadc_inst;
int xsts;
char *channel[] ={"VAUX14","VAUX07","VAUX15","VAUX06"}; //for RawData printf
int sample[4] = {XSM_CH_AUX_MIN + 14,XSM_CH_AUX_MIN + 7,XSM_CH_AUX_MIN + 15,XSM_CH_AUX_MIN + 6};
//sample array used to specify channel when reading ADC data into XADC_Buf
int main()
{
	XGpio gpio;
	XGpio gpio1;
	XGpio gpio2;
	XGpio gpio3;
	u32 btn, led;
	u32 sw;
	u32 jbin, digin, rpiin;
    u32 jcout;
	XGpio_Initialize(&gpio, 0); //buttons and leds
	XGpio_Initialize(&gpio1, 1); //switches
	XGpio_Initialize(&gpio2, 2); //JB connector
	XGpio_Initialize(&gpio3, 3); //JC connector
	
	XGpio_SetDataDirection(&gpio, 2, 0x00000000); // set led GPIO channel tristates to All Output
	XGpio_SetDataDirection(&gpio, 1, 0xFFFFFFFF); // set BTN GPIO channel tristates to All Input
	XGpio_SetDataDirection(&gpio1, 1, 0xFFFFFFFF); // set sw GPIO channel tristates to All Input
	XGpio_SetDataDirection(&gpio2, 1, 0xFFFFFFFF); // set JB GPIO channel tristates to All Input
	XGpio_SetDataDirection(&gpio3, 1, 0x00000000); // set JC GPIO channel tristates to All Output
	int Index;
	XSysMon *xadc_inst_ptr = &xadc_inst;
	u32 XADC_Buf[RX_BUFFER_SIZE];


	XSysMon_Config *xadc_config;

//	init_platform();

	xil_printf("XADC Example\n\r");

	xadc_config = XSysMon_LookupConfig(xadc);
	if (NULL == xadc_config){
		xil_printf("XSysMon_LookupConfig failed\n");
	}

	XSysMon_CfgInitialize(xadc_inst_ptr,xadc_config,xadc_config->BaseAddress);

	xsts=XSysMon_SelfTest(xadc_inst_ptr);
	if (XST_SUCCESS != xsts){
		xil_printf("ADC self test failed\n");
	}
	XSysMon_SetSequencerMode(xadc_inst_ptr,XSM_SEQ_MODE_SAFE);
	XSysMon_SetAlarmEnables(xadc_inst_ptr, 0x00000000);
	XSysMon_SetSequencerMode(xadc_inst_ptr,XSM_SEQ_MODE_SAFE);
	XSysMon_SetAlarmEnables(xadc_inst_ptr, 0x0);
	xsts = XSysMon_SetSeqChEnables(xadc_inst_ptr,
				XSM_SEQ_CH_AUX14 |
				XSM_SEQ_CH_AUX07 |
				XSM_SEQ_CH_AUX15 |
				XSM_SEQ_CH_AUX06);
	if (XST_SUCCESS != xsts){
			xil_printf("Failed to configure XSysMon_SetSeqChEnables\n");
	}
	xsts=XSysMon_SetSeqInputMode(xadc_inst_ptr,0);
	if (XST_SUCCESS != xsts){
		xil_printf("Failed to configure all XADC channels as unipolar\n");
	}
	XSysMon_SetSequencerMode(xadc_inst_ptr,XSM_SEQ_MODE_CONTINPASS);
	
	
	/** Here's where the fun begins **/
	
	u32 digital_buffer = 0;
	u32 analog_buffer  = 0;
	
	#define analog_pin 2

	for (;;) {
		digital_buffer = 0;
		analog_buffer  = 0;
	
		for (int i = 0; i < 32; i++) {
//			btn = XGpio_DiscreteRead(&gpio, 1);
//			sw  = XGpio_DiscreteRead(&gpio1,1);
		
			jbin  = XGpio_DiscreteRead(&gpio2,1);
			digin = jbin & 0xF; //jb[3..0]
			rpiin = (jbin & 0xF0)>>4; //jb[7..4];
			
			digital_buffer |= !(digin&1) << i;
			analog_buffer  |= ((XSysMon_GetAdcData(xadc_inst_ptr,sample[analog_pin])>>4) < 3000) << i;
		
			XGpio_DiscreteWrite(&gpio, 2, sw);
			XGpio_DiscreteWrite(&gpio3, 1, !(digin&1));

			usleep_MB(10000);
		}
		
		xil_printf("Digital: %08x\r\n", digital_buffer);
		xil_printf("Analog: %08x\r\n",  analog_buffer);
		xil_printf("\n");
	}

#if 0
	while(1){

		/*********PushButton, Switch, and Led Section*/
		btn = XGpio_DiscreteRead(&gpio, 1);
		sw  = XGpio_DiscreteRead(&gpio1,1);
		jbin  = XGpio_DiscreteRead(&gpio2,1);
	//	jcout = 2;//set to 0 for silence, 3 for high frequency buzzer
				
		digin = jbin & 0xF; //jb[3..0]
		rpiin = (jbin & 0xF0)>>4; //jb[7..4];
		
		if (btn != 0) // turn all LEDs on when any button is pressed
			led = sw;
		else
			led = 0x00000000;
		
		jcout = 0;	
		if(!(rpiin &1 && digin &1))
			jcout = 1;//set to 0 for silence, 3 for high frequency buzzer
		
		XGpio_DiscreteWrite(&gpio, 2, led);
		XGpio_DiscreteWrite(&gpio3, 1, jcout);
		
		//xil_printf("\r jbin: %08x, digin: %08x, rpiin: %08x\n",jbin,digin,rpiin);

		xil_printf("\rbutton state: %08x\n",btn);
		xil_printf("\r jbin: %08x, digin: %08x, rpiin: %08x\n",jbin,digin,rpiin);
		//xil_printf("   \n");
		
		xil_printf("\r: \n");

		/******************end of section*************/

		 /*****************************XADC section**************/
		XSysMon_GetStatus(xadc_inst_ptr); //Clear the old status
		for (Index = 0;Index<RX_BUFFER_SIZE;Index++){
			while((XSysMon_GetStatus(xadc_inst_ptr)& XSM_SR_EOS_MASK) != XSM_SR_EOS_MASK){
				XADC_Buf[Index] = XSysMon_GetAdcData(xadc_inst_ptr,sample[Index]);
			//xil_printf("Voltage %s = %d\n",channel[Index],XSysMon_RawToVoltage(XADC_Buf[Index]));
			}
		}

		for(Index = 0;Index<RX_BUFFER_SIZE;Index++){
		//xil_printf("Voltage=%d %s\n",channel[Index],XSysMon_RawToVoltage(XADC_Buf[Index]));
		    xil_printf("RawData %s %d \n",channel[Index],(int)(XADC_Buf[Index]>>4));
		}
		xil_printf("   \n");
		sleep(1);

//		usleep_MB(1000);
		/****************end of section*************/
	} //end of while(1)
#endif
	return 0;
}
