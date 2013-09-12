#-*- coding=utf8 -*-
import serial
import sys
def execute(command):
	ser = serial.Serial(0,timeout=0.5)
	ser.write(command+"\r\n")
	return ser.readlines()

def decodePDU(pdu):
    """    
	    return {"SmsCenter":SmsCenter,
            "Sender":Sender,
            "TPPID":TPPID,
            "TPDCS":TPDCS,
            "TimeStamp":TimeStamp,
            "TPUserDataLength":TPUserDataLength,
            "Content":Content}
    """
    SmsCenterLen= 2 * int(pdu[:2])
    SmsCenter = ReverseNumber(pdu[4 : 2 + SmsCenterLen])
    #print "SmsCenter: %s" % SmsCenter
    SenderLen = int(pdu[2 + SmsCenterLen + 2 : 2 + SmsCenterLen + 4],16)
    if SenderLen % 2 != 0:
	    SenderLen = SenderLen + 1
    Sender = ReverseNumber(pdu[2 + SmsCenterLen + 6 : 2 + SmsCenterLen + 6 +  SenderLen ])
    #print "Sender : %s" % Sender
    TPPID = pdu[2 + SmsCenterLen + 6 + SenderLen : 2 + SmsCenterLen + 6 + SenderLen + 2]
    #print "TPPID : %s" % TPPID
    TPDCS = pdu[ 2 + SmsCenterLen + 6 + SenderLen + 2 :  2 + SmsCenterLen + 6 + SenderLen + 2 + 2]
    #print "TPDCS : %s" %TPDCS
    TimeStamp = pdu [ 2 + SmsCenterLen + 6 + SenderLen + 2 + 2 :  2 + SmsCenterLen + 6 + SenderLen + 2 + 2 + 14]
    #print "TimeStamp : %s" % TimeStamp
    TPUserDataLength = int(pdu[2 + SmsCenterLen + 6 + SenderLen + 2 + 2 + 14 : 2 + SmsCenterLen + 6 + SenderLen + 2 + 2 + 14 + 2],16)
    #print "TPUserDataLength : %s" % TPUserDataLength
    Content = pdu[2 + SmsCenterLen + 6 + SenderLen + 2 + 2 + 14 + 2 : ]
    #print "Content : %s" % Content
    Content = ucps2str(Content)

    return {"SmsCenter":SmsCenter,
            "Sender":Sender,
	    "TPPID":TPPID,
            "TPDCS":TPDCS,
	    "TimeStamp":TimeStamp,
	    "TPUserDataLength":TPUserDataLength,
	    "Content":Content}

def ReverseNumber(number):
    a = "" # Reverse SmsCenter char every 2
    for i in range(len(number)/2):
        a = a + number[2*i+1]
        a = a + number[2*i]
    if a.endswith("F"): # remove the finale "F"
	a = a[:-1]
    return a 

def ucps2str(ucpstr):
    """Convert unicode code point(in hex) ascii string to unicode string"""
    s = ''
    for i  in range(len(ucpstr)/4):
        ucp = ucpstr[i*4:i*4+4]
        s = s + unichr(int(ucp,16))
    return s

def str2ucps(ucpstr):
    """ Convert unicode string to hex string"""
    s = ''
    ucpstr=unicode(ucpstr).decode('utf-8')
    for i in ucpstr:
        s = s + "%04X" % ord(i)
    return s
        
def EncodeSMSCenterNumber(t):
    """ reverse number Auto add F if not odd.. """
    s = ''
    t = str(t)
    if len(t) % 2 != 0:
        t = t + 'F'
        F_Added = True

    for i in range(len(t)/2):
        s = s + t[2*i + 1]
        s = s + t[2*i]

    s = '91' + s
    
    s = "%02X" %(len(s)/2) +  s

    return s

def EncodeOutNumber(t):
    """ reverse number Auto add F if not odd.. """
    s = ''
    t = str(t)
    F_Added = False
    if len(t) % 2 != 0:
        t = t + 'F'
        F_Added = True

    for i in range(len(t)/2):
        s = s + t[2*i + 1]
        s = s + t[2*i]

    pre = len(s)
    if F_Added:
        pre = pre - 1

    s = "%02X" % pre + '91' + s
    return s
    
def send2str(OutNum,TEXT):

    """OutNum eg:13802938402,donot add +86 , TEXT needs to be unicode eg: u"blah"  return (CMGS_len,PDUCodeString)"""

    smscenter = EncodeSMSCenterNumber('8613800371500')
    OutNum = str(OutNum)
    TEXT = unicode(TEXT)
    if OutNum.startswith('86') and OutNum.len==13:
        OutNum = OutNum
    else:
        OutNum ='86' + OutNum 

    outNumber = '001100' + EncodeOutNumber(OutNum)

    message = str2ucps(TEXT)
    message = "%02X" % (len(message)/2) + message

    PDUCodeString =  outNumber + '0008AA' + message
    CMGS_len = len(PDUCodeString)/2 - 1
    return (CMGS_len,PDUCodeString)

	    
if __name__=="__main__":
    print "pdu.py: __main__"
    print send2str('10086',u'你好这是短信猫上来的短信哦，可好玩了')
