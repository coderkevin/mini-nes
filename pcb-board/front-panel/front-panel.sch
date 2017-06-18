EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:e-switch
LIBS:Mini-NES_Panel-cache
EELAYER 25 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "Mini-NES_NFC_FRONT-PANEL by @coderkevin"
Date "2017-05-18"
Rev "1.0"
Comp "Eladio Martinez"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_01X05 J1
U 1 1 591E5B6A
P 2800 4700
F 0 "J1" H 2800 5000 50  0000 C CNN
F 1 "FRONT_CONN" V 2900 4700 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x05_Pitch2.54mm" H 2800 4700 50  0001 C CNN
F 3 "" H 2800 4700 50  0001 C CNN
	1    2800 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	8450 2450 8450 2100
Connection ~ 7850 2450
Text Label 2600 4500 2    60   ~ 0
GND
Text Label 2600 4600 2    60   ~ 0
VCC
Text Label 8250 4450 0    60   ~ 0
LED
Text Label 2600 4800 2    60   ~ 0
PWR
Text Label 2600 4900 2    60   ~ 0
RST
Text Label 2350 1950 2    60   ~ 0
RST
Text Label 7450 2000 2    60   ~ 0
PWR
Text Label 8050 2000 2    60   ~ 0
LED
$Comp
L LED D1
U 1 1 591E600E
P 8050 4450
F 0 "D1" H 8050 4550 50  0000 C CNN
F 1 "LED" H 8050 4350 50  0000 C CNN
F 2 "LEDs:LED_D3.0mm" H 8050 4450 50  0001 C CNN
F 3 "" H 8050 4450 50  0001 C CNN
	1    8050 4450
	1    0    0    -1  
$EndComp
Text Label 2750 1850 0    60   ~ 0
GND
NoConn ~ 8450 1900
Text Notes 5700 1050 0    118  ~ 0
Power Button
$Comp
L R R1
U 1 1 591F3340
P 7700 4650
F 0 "R1" V 7780 4650 50  0000 C CNN
F 1 "220h" V 7700 4650 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal" V 7630 4650 50  0001 C CNN
F 3 "" H 7700 4650 50  0001 C CNN
	1    7700 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 4450 8200 4450
$Comp
L TL2230OA SW1
U 1 1 591F3F8D
P 2550 1950
F 0 "SW1" H 2550 2120 50  0000 C CNN
F 1 "TL2230OA" H 2550 1750 50  0000 C CNN
F 2 "e-switch:TL2230" H 2550 1950 50  0001 C CNN
F 3 "" H 2550 1950 50  0001 C CNN
	1    2550 1950
	1    0    0    -1  
$EndComp
$Comp
L TL2230EE SW2
U 1 1 591F4014
P 7650 2000
F 0 "SW2" H 7650 2170 50  0000 C CNN
F 1 "TL2230EE" H 7650 1800 50  0000 C CNN
F 2 "e-switch:TL2230" H 7650 2000 50  0001 C CNN
F 3 "" H 7650 2000 50  0001 C CNN
	1    7650 2000
	1    0    0    -1  
$EndComp
$Comp
L TL2230EE SW2
U 2 1 591F40A7
P 8250 2000
F 0 "SW2" H 8250 2170 50  0000 C CNN
F 1 "TL2230EE" H 8250 1800 50  0000 C CNN
F 2 "e-switch:TL2230" H 8250 2000 50  0001 C CNN
F 3 "" H 8250 2000 50  0001 C CNN
	2    8250 2000
	1    0    0    -1  
$EndComp
Text Notes 750  1050 0    118  ~ 0
Reset Button
Text Label 8450 2100 0    60   ~ 0
VCC
Wire Wire Line
	7850 2100 7850 2450
Text Label 2600 4700 2    60   ~ 0
LED
Text Label 7950 4900 0    60   ~ 0
GND
Text Label 7850 1700 0    60   ~ 0
GND
Wire Wire Line
	7850 1900 7850 1700
Text Label 2750 2050 0    60   ~ 0
VCC
Wire Wire Line
	7850 2450 8450 2450
Wire Notes Line
	10500 3300 450  3300
Wire Notes Line
	5350 450  5350 6200
Wire Notes Line
	450  6200 10550 6200
Text Notes 5750 3900 0    118  ~ 0
Power LED
Text Notes 800  3900 0    118  ~ 0
Connector
Text Notes 8950 3100 0    60   ~ 0
Note: Latching push button
Text Notes 3750 3100 0    60   ~ 0
Note: Momentary push button
Wire Wire Line
	7900 4450 7700 4450
Wire Wire Line
	7700 4450 7700 4500
Wire Wire Line
	7700 4800 7700 4900
Wire Wire Line
	7700 4900 7950 4900
$EndSCHEMATC
