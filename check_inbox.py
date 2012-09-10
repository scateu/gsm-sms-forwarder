#coding:UTF-8
# modified : scateu @ 2012-8-10 16:00
import serial
import sys
import time
from pdu import send2str
from messaging.sms import SmsDeliver
from mymail import mymail
reload(sys)
sys.setdefaultencoding('UTF-8')
output_coding = 'gbk'

InboxIsEmpty = False
SMSCenter = "13800531500"
SerialPort = "COM1"
output_buffer = ""

def execute(command,timeout=0.5,raw=False):
    ser = serial.Serial(SerialPort,baudrate=115200,timeout=timeout)
    if raw :
        ser.write(command)
    else:
        ser.write(command+"\r\n")
    return ser.readlines()

def WriteLog(string):
    global output_buffer
    print string
    output_buffer += string
    output_buffer += '\n'
    
    
def DeleteSMS(number):
    if execute("AT+CMGD=" + str(number) + ";")[1].startswith("OK"):
        WriteLog("SMS #%d"%number + "Deleted")

def ShowLatestSMS(AutoDelete = False):
    """
    Fetch Latest SMS
    
    ShowLatestSMS(AutoDelete = False)

        return False when empty
    """
    #WriteLog("Latest SMS as following: ")

    # Firstly, Get all sms, and their ID
    global InboxIsEmpty
    results = execute("AT+CMGL=4")
    smsids = []
    cmgl = [r for r in results if r.startswith("+CMGL")]
    for a in cmgl:
        smsids.append( int(a.split(",")[0].replace("+CMGL:","")) )
    
    if len(cmgl) == 0:
        ShowTime()
        WriteLog("Empty. No SMS")
        InboxIsEmpty = True
        return False

    currentid =  str(smsids.pop())
    results = execute("AT+CMGR="+ currentid + ";")
    if results[2].startswith("08") != True :
        WriteLog("ERROR")
    ShowTime()
    WriteLog(":::::: SMS # " + currentid + " ::::::")
    pducode = results[2].replace('\r\n','')
    pduresult = SmsDeliver(pducode)

    WriteLog("Sender: " + str(pduresult.number))
    #WriteLog(pduresult.text.decode('utf8','ignore').encode('utf8')
    WriteLog(pduresult.text.decode('utf8','ignore').encode(output_coding))

    if AutoDelete:
            DeleteSMS(int(currentid))
        
    return False if  len(smsids) == 0 else True

def Call(number):
    ShowTime()
    WriteLog("Calling " + str(number) )
    if execute("ATD"+' '+str(number)+";")[-1].startswith("OK") : 
        ShowTime()
        WriteLog("Call Success.")
    else: 
        ShowTime()
        WriteLog("Call Maybe Failed." )
        
def ShowTime():
    WriteLog(time.strftime('%Y-%m-%d %H:%M:%S'))


def ReadAll():
    global output_buffer
    output_buffer = ''
    while ShowLatestSMS(AutoDelete=True):
        ShowLatestSMS(AutoDelete=True)
    # return something

def SendSMS(Number,TEXT):
    pdu = send2str(Number,unicode(TEXT))
    ShowTime()
    WriteLog("Sending Message")
    WriteLog("Number : " + str(Number))
    WriteLog("TEXT: " + unicode(TEXT))
    AT_CMGS_LEN = pdu[0]
    PduCode = pdu[1]
    execute("AT")
    execute("AT+CMGF=0")
    execute('AT+CSCA="' + SMSCenter + '"') # SMS Center
    execute("AT+CMGS="+str(AT_CMGS_LEN))
    execute(PduCode,raw=True)
    execute(b'\32',raw=True)  # Ctrl + Z
    return ''

def check(receiver):
    WriteLog("...:::::: %s ::::::..."%time.ctime())
    ReadAll()
    global output_buffer
    #print output_buffer.find('Empty')
    if output_buffer.find('Sender') != -1: # not empty
        f = open('log.txt','a')
        f.write(output_buffer)
        f.close()
        m = mymail()
        m.sendmail(to=receiver,subject='Your SMS - %s '%time.ctime(),message=output_buffer.decode('gbk').encode('utf8'))


if __name__=="__main__":
    while True:
        check(receiver='blah@gmail.com')
        sleeptime = 30
        print 'Next check in: %d'%sleeptime,
        while sleeptime >0:
            time.sleep(1)
            sleeptime -= 1
            print sleeptime,
        print ''
