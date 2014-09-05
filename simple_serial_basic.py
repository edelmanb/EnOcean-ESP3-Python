#!/usr/bin/python
import serial
import os
import sys

u8CRC8Table = [
  0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 
  0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, 
  0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 
  0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, 
  0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 
  0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, 
  0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 
  0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, 
  0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 
  0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, 
  0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 
  0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, 
  0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 
  0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, 
  0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 
  0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, 
  0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 
  0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, 
  0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 
  0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, 
  0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 
  0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, 
  0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 
  0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, 
  0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 
  0x76, 0x71, 0x78, 0x7f, 0x6A, 0x6d, 0x64, 0x63, 
  0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 
  0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, 
  0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 
  0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8D, 0x84, 0x83, 
  0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 
  0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]

def proccrc8(CRC, u8Data): 
	return u8CRC8Table[(CRC ^ u8Data) & 0xff]; 
	
def printHeader(dataLength,opDataLength,packetType,headerCRC):
	print("Header:",int(dataLength,16),int(opDataLength,16),int(packetType,16),headerCRC)
	return
def printSerialData(serialData):
	print("Serial Data: ", serialData[0:int(dataLength,16)*2])
	return

def printPacketType1(serialData):
	strRorg = "RORG: "
	strRorg += serialData[0:2]
	print strRorg
	
	strData = "Data: "
	if strRorg[len(strRorg)-2:len(strRorg)] == 'f6':
		strData += serialData[2:4]
		strSrcId = "Source ID: "
		strSrcId += serialData[4:12]
		print strSrcId
		
	elif strRorg[len(strRorg)-2:len(strRorg)] == 'a5':
		strData += serialData[2:10]
		strSrcId = "Source ID: "
		strSrcId += serialData[10:18]
		print strSrcId
	else:
		()
	print strData + "\n"
	return

def printOpData():
	return

def checkHeaderCRC():
	u8CRCHeader = 0
	
	u8CRCHeader = ( proccrc8(u8CRCHeader, int(dataLength,16)>>8))
	u8CRCHeader = ( proccrc8(u8CRCHeader, int(dataLength,16)&0xff))
	u8CRCHeader = ( proccrc8(u8CRCHeader, int(opDataLength,16)))
	u8CRCHeader = ( proccrc8(u8CRCHeader, int(packetType,16)))

	if u8CRCHeader == int(headerCRC,16):
		return True
	else:
		return False

def checkDataCRC(serialData):
	u8CRCData = 0
	i = 0

	while (i<len(serialData)-2):
		u8CRCData = proccrc8(u8CRCData, (int(serialData[i]+serialData[i+1],16)&0xff))
		i=i+2
	
	if (u8CRCData == int(serialData[len(serialData)-2]+serialData[len(serialData)-1],16)):
		return True
	else:
		return False
		
def checkPacketType( x):
		if packetType == x: #x is 'x'
			return True
		else:
			return False
			
def getSerialData():
	global dataLength, opDataLength, packetType, headerCRC,totalDataLength, serialData   
	s = 0
	i = 0
	while s != '55':
		if ser.inWaiting() != 0: 
			s = ser.read(1).encode("hex")
	
	while ser.inWaiting() < 5:  
		()
	dataLength = ser.read(2).encode("hex") #read length field
	opDataLength = ser.read(1).encode("hex") #read op length field
	packetType = ser.read(1).encode("hex") #read packet type field
	headerCRC = ser.read(1).encode("hex") #read header crc field

	if (checkHeaderCRC()):	
		totalDataLength = (int(dataLength,16) + int(opDataLength,16))
	
		while ser.inWaiting() < totalDataLength:  
			()
			
		serialData = ser.read(totalDataLength+1).encode("hex")	
		if checkDataCRC(serialData): 
			return serialData	
		return "Data CRC Failed"
	return "Header CRC Failed"
	
def calcESP3HeaderCRC(telegramHeader):
	u8CRC = 0;
	u8CRC = proccrc8(u8CRC,telegramHeader[1])
	u8CRC = proccrc8(u8CRC,telegramHeader[2])
	u8CRC = proccrc8(u8CRC,telegramHeader[3])
	u8CRC = proccrc8(u8CRC,telegramHeader[4])
	return u8CRC
	
def calcESP3DataCRC(telegramData):
	u8CRC = 0;
	for index in range(len(telegramData)):
		u8CRC = proccrc8(u8CRC,telegramData[index])

	return u8CRC


def calcESP3Header(packetType,packetData, *arg): #assumes 0 optional data
	pHeader = [0x55] #sync
		#for now we support max of 255 byte packets
	pHeader.append(0x00) #MSB Data Length
	pHeader.append(len(packetData))#LSB Data Length
	if len(arg) == 0:
		pHeader.append(0x00) #optional data length
	else:
		pHeader.append(arg[0])
	pHeader.append(packetType) #packet type
	pHeader.append(calcESP3HeaderCRC(pHeader))# Header CRC
	return pHeader
		
def sendESP3Packet(packetType, packetData):
	pESP3Packet = calcESP3Header(packetType,packetData)
	pESP3Packet += packetData 
	pESP3Packet.append(calcESP3DataCRC(packetData))
	
	for index in range(len(pESP3Packet)):
		pESP3Packet[index] = chr(pESP3Packet[index])
		#byte by byte tx
		ser.write(pESP3Packet[index])				
	return getSerialData()		

def sendTest():
	ser.write("\x55\x00\x07\x00\x01\x11\xD5\x55\x00\x00\x00\x00\x80\x5A")

	
#common commands

def commandReadVersion(): 
	returnData = sendESP3Packet(0x05, [0x03])	
	
	if int(returnData[0:1],16) == 0x00:
		tmpStr = "Application Version: " + str(int(returnData[2:4],16)) \
		+ '.' + str(int(returnData[4:6],16)) + '.' + str(int(returnData[6:8],16)) \
		+ '.' + str(int(returnData[8:10],16))
		print tmpStr
		
		tmpStr = "API Version: " + str(int(returnData[10:12],16)) \
		+ '.' + str(int(returnData[12:14],16)) + '.'+ str(int(returnData[14:16],16))+ '.'+ str(int(returnData[16:18],16))
		print tmpStr
		
		print "Chip ID:",returnData[18:26]
		
		i = 34
		tmpStr = "Application: "
		while chr(int(returnData[i]+returnData[i+1],16)) != "\0":
			tmpStr+=(chr(int(returnData[i]+returnData[i+1],16)))
			i = i + 2
		print tmpStr
		
		return True
	else:
		print "Response Error:" + returnData[0]
		return False
	
		
def commandReadBaseId(): 
	returnData = sendESP3Packet(0x05, [0x08])		
	
	if int(returnData[0:1],16) == 0x00:
		tmpStr = "BaseId: "
		i = 2
		while i < 10:
			tmpStr += returnData[i]+returnData[i+1]
			i = i + 2
		print tmpStr
	
		tmpStr = "Base Id Writes Remaining: " 
		tmpStr += returnData[10]+returnData[11]
		print tmpStr
	else:
		print "Response Error:" + returnData[0]
	
	
def main():	
	global ser 
	print "Welcome to ESP3 with python\n"
	
	os.system("python -m serial.tools.list_ports \n")
	var = raw_input("\nEnter Serial Port: ")
	ser = serial.Serial(var, 57600, timeout = 0)  # open serial port

	if commandReadVersion() != True:
		print "Communication not successful - exiting"
		sys.exit(0)
	commandReadBaseId()
	

	while (True):
		getSerialData()
		if checkPacketType('01'):
			printPacketType1(serialData)
	
if __name__ == "__main__":
    main()
