#!/usr/bin/python
# -*- coding: utf8 -*-

email_user = "blalblahh@126.com"
email_password = "blahblah"
smtp_server = "smtp.blahblah.com"
smtp_port = 25

import smtplib
class mymail():
    """
    Library to sendmail from ramlab_things@126.com
    see sendmail()
    """
    def __init__(self):
        self.email_user = email_user
        self.email_password = email_password

    def sendmail(self,to,subject,message):
        """
        to = 'scateu@gmail.com'
        subject = 'blahblah'
        message = 'blahblah'
        m = ramlab_mail()
        m.sendmail(to='scateu@gmail.com',subject='blah',message='bye.')
        """
        self.smtpserver = smtplib.SMTP(smtp_server,smtp_port)
        self.smtpserver.ehlo()
        self.smtpserver.starttls()
        self.smtpserver.ehlo
        self.smtpserver.login(self.email_user, self.email_password)
        self.header = 'To:' + to + '\n' + 'From: ' + self.email_user + '\n' + 'Subject:' + subject +'\n'
        self.msg = self.header + '\n' + message + '\n\n'
        self.smtpserver.sendmail(self.email_user,to,self.msg)
        print 'email sent.'
        self.smtpserver.close()

if __name__ == "__main__":
    m = mymail()
    m.sendmail(to='scateu@126.com,scateu@gmail.com',subject='blah',message=u'哈哈.'.encode('utf8'))
