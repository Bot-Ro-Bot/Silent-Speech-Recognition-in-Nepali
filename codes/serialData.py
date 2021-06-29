from serial import Serial
import binascii

class interfaceOpenBCI(Serial):
	# def __init__(self, arg):
	def getInitialStatus(self):
		receivedString=''
		initialMessageReceived=False
		timeoutTrigger = 0
		while not initialMessageReceived:
			receivedByte = super().read().decode()
			print(" byt : ", receivedByte)
			if receivedByte == '':
				timeoutTrigger+=1
				if timeoutTrigger > 3:
					print("[-] Message not received")
					return False
			receivedString += receivedByte
			if '$$$' in receivedString:
				initialMessageReceived = True
				print(receivedString)
				print("[+] Initial message received")
				return True


	def setToDigitalMode(self):
		toDigitalModeCommand = '/3'.encode()
		super().write(toDigitalModeCommand)
		receivedString=''
		initialMessageReceived=False
		while not initialMessageReceived:
			receivedByte = super().read()
			receivedString += receivedByte.decode()
			if '$$$' in receivedString:
				initialMessageReceived = True
		print(receivedString)
		return True 

	def startRecording(self):
		readCommand = 'b'.encode()
		super().write(readCommand)

	def readRaw(self):
		while True:
			receivedByte = ser.read(1)
			# print(receivedBytes.decode(),end='')
			print(binascii.hexlify(receivedByte))

	def capturePacket(self):
		'''
		range	byte 	remarks		codes
		1		1 		start byte 	 A0
		2 		1 		Sample #	 --
		3-5 	3		EXG 1 		 -- -- --
		6-8 	3 		EXG 2 		 -- -- --
		9-11	3 		EXG 3        -- -- --
		12-14	3 		EXG 4        -- -- --
		15-17	3 		EXG 5        -- -- --
		18-20	3 		EXG 6        -- -- --
		21-23	3 		EXG 7        -- -- --
		24-26	3 		EXG 8        -- -- --
		#Aux packet option are Accelerometer, digital, analog and have to set modes
		27
		28
		29
		30
		31
		32

		# end byte 		- xCX - X - depends upon mode, Making digital read the default mode probably 
		33		1 		end byte 	 C0
		'''

DEVICE_PORT_NAME = '/dev/ttyUSB0'
BAUD_RATE = 115200
PARITY = 8 
TIMEOUT = 2 	#seconds

openbci = interfaceOpenBCI(DEVICE_PORT_NAME, BAUD_RATE, timeout=TIMEOUT)
openbci.getInitialStatus()
openbci.setToDigitalMode()
# openbci.startRecording()

