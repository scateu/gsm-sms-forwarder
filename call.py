#!/usr/bin/python
#-*- coding:utf-8 -*-
import serial
import sys
import time
from pdu import decodePDU
reload(sys)
sys.setdefaultencoding('UTF-8')

AlertNumber = str(sys.argv[-1])
SerialPort = "COM1"
def execute(command,timeout=0.5):
	ser = serial.Serial(SerialPort,baudrate=115200,timeout=timeout)
	ser.write(command+"\r\n")
	return ser.readlines()
	
def Call(number):
	SmsInboxBuffer=[]
	ShowTime()
	print "Calling " + str(number) 
	if execute("ATD"+' '+str(number)+";")[-1].startswith("OK") : 
		ShowTime()
		print "Call Success."
	else: 
		ShowTime()
		print "Call Maybe Failed." 
def ShowTime():
	print time.strftime('%Y-%m-%d %H:%M:%S'),

def Hangup():
	print "Hangup.."
	execute("ATZ")

if __name__=="__main__":
	Call(AlertNumber)
	time.sleep(10)
	Hangup()
