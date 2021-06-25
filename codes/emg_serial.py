import serial
import binascii
from serial.tools import list_ports 
portLists = list_ports.main()
print(portLists)

devicePortName = '/dev/ttyUSB0'
baudRate = 115200
parity = 8 
timeout = 2 	#seconds

samplesNumber = 100

with serial.Serial(devicePortName, baudRate, timeout=timeout) as ser:
	receivedString = ''
	initialMessageReceived = False
	while not initialMessageReceived:
		receivedByte = ser.read()
		# print('time out triggered.')
		receivedString += receivedByte.decode()
		if '$$$' in receivedString:
			initialMessageReceived = True
	print(receivedString)
	print("[+] Initial message received")

	readCommand = 'b'.encode()
	ser.write(readCommand)

	while True:
		receivedByte = ser.read(1)
		# print(receivedBytes.decode(),end='')
		print(binascii.hexlify(receivedByte))



'''
Sample Index, 	EXG Channel 0, 	EXG Channel 1, 		EXG Channel 2, 		EXG Channel 3, 		EXG Channel 4, 		EXG Channel 5, 
229.0, 			-33375.78125, 	10337.591796875, 	5964.29443359375, 	18111.841796875, 	7371.42626953125, 	14257.4619140625, 

EXG Channel 6, 		EXG Channel 7, 		Accel Channel 0, 	Accel Channel 1, 	Accel Channel 2, 	Other, 	Other, 	Other, 	Other, 
30150.244140625, 	12550.146484375, 	0.0, 				0.0, 				0.0, 				193.0, 	0.0, 	1.0, 	1.0, 

Other, 	Other, 	Other, 	Analog Channel 0, 	Analog Channel 1, 	Analog Channel 2, 	Timestamp, 				Timestamp (Formatted)
0.0, 	0.0, 	1.0, 	1.0, 				256.0, 				1.0, 				1.620898581782125E9, 	2021-05-13 15:21:21.782


b'a0'
b'91'
b'92'
b'10'
b'46'
b'ab'
b'f3'
b'7d'
b'91'
b'a9'
b'a5'
b'91'
b'89'
b'b0'
b'ad'
b'ba'
b'92'
b'a2'
b'88'
#'''