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
EELAYER 25 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "Mini-NES_NFC by @coderkevin"
Date "2017-05-18"
Rev "1.0"
Comp "Eladio Martinez"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_02X08 J2
U 1 1 591DF53B
P 3250 3350
F 0 "J2" H 3250 3800 50  0000 C CNN
F 1 "RPi3 GPIO" V 3250 3350 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_2x08_Pitch2.54mm" H 3250 2150 50  0001 C CNN
F 3 "" H 3250 2150 50  0001 C CNN
	1    3250 3350
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 591DF7AE
P 8700 3600
F 0 "R1" V 8780 3600 50  0000 C CNN
F 1 "10K" V 8700 3600 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 8630 3600 50  0001 C CNN
F 3 "" H 8700 3600 50  0001 C CNN
	1    8700 3600
	0    -1   -1   0   
$EndComp
$Comp
L CONN_01X04 J1
U 1 1 591DF89C
P 8750 1400
F 0 "J1" H 8750 1650 50  0000 C CNN
F 1 "NFC READER" V 8850 1400 50  0000 C CNN
F 2 "Connectors_Molex:Molex_PicoBlade_53047-0410_04x1.25mm_Straight" H 8750 1400 50  0001 C CNN
F 3 "" H 8750 1400 50  0001 C CNN
	1    8750 1400
	1    0    0    -1  
$EndComp
Text Label 8550 1250 2    60   ~ 0
GND
Text Label 8550 1350 2    60   ~ 0
VCC
Text Label 8550 1450 2    60   ~ 0
SDA
Text Label 8550 1550 2    60   ~ 0
SCL
Text Label 3000 3000 2    60   ~ 0
VCC
Text Label 3000 3400 2    60   ~ 0
GND
Text Label 3000 3100 2    60   ~ 0
SDA
Text Label 3000 3200 2    60   ~ 0
SCL
NoConn ~ 3000 3300
$Comp
L CONN_01X02 J3
U 1 1 591E03C4
P 8700 3100
F 0 "J3" H 8700 3250 50  0000 C CNN
F 1 "RESET PIN" V 8800 3100 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_1x02_Pitch2.54mm" H 8700 3100 50  0001 C CNN
F 3 "" H 8700 3100 50  0001 C CNN
	1    8700 3100
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8550 3600 8550 3400
Wire Wire Line
	8650 3400 8650 3300
Wire Wire Line
	8750 3300 8750 3400
Wire Wire Line
	8750 3400 8850 3400
Wire Wire Line
	8850 3400 8850 3600
Wire Wire Line
	8350 3400 8650 3400
Text Label 3000 3700 2    60   ~ 0
LED
Text Label 8350 3400 2    60   ~ 0
LED
Connection ~ 8550 3400
NoConn ~ 3500 3000
NoConn ~ 3500 3100
NoConn ~ 3500 3200
NoConn ~ 3500 3400
NoConn ~ 3500 3500
NoConn ~ 3500 3600
NoConn ~ 3500 3700
NoConn ~ 3500 3300
Text Notes 6600 800  0    118  ~ 0
NFC Reader
Text Notes 6600 2700 0    118  ~ 0
Reset Pin
Text Notes 1050 1200 0    118  ~ 0
Raspberry GPIO
Text Notes 6550 4700 0    118  ~ 0
Front Pannel
$Comp
L CONN_01X05 J4
U 1 1 591E40B0
P 8750 5300
F 0 "J4" H 8750 5600 50  0000 C CNN
F 1 "FRONT PANEL" V 8850 5300 50  0000 C CNN
F 2 "Connectors_Molex:Molex_PicoBlade_53047-0510_05x1.25mm_Straight" H 8750 5300 50  0001 C CNN
F 3 "" H 8750 5300 50  0001 C CNN
	1    8750 5300
	1    0    0    -1  
$EndComp
Text Label 8550 5100 2    60   ~ 0
GND
Text Label 8550 5200 2    60   ~ 0
VCC
Text Label 8550 5300 2    60   ~ 0
LED
Text Label 8550 5400 2    60   ~ 0
PWR
Text Label 3000 3600 2    60   ~ 0
PWR
Text Label 8550 5500 2    60   ~ 0
RST
Text Label 3000 3500 2    60   ~ 0
RST
Wire Notes Line
	500  6300 10550 6300
Wire Notes Line
	6300 500  6300 6300
Wire Notes Line
	6300 6300 6350 6300
Wire Notes Line
	10500 4350 6300 4350
Wire Notes Line
	10550 2350 6300 2350
$EndSCHEMATC
