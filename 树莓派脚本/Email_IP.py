#/bin/env python
# -*-coding:utf8-*-
import socket
import fcntl
import time
import struct
import smtplib
import urllib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


#发送邮件的基本函数，参数依次如下
# smtp服务器地址、邮箱用户名，邮箱秘密，发件人地址，收件人地址（列表的方式），邮件主题，邮件html内容
def sendEmail(smtpserver, username, password, sender, receiver, subject, msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] =  subject
    msgText = MIMEText(msghtml,'html','utf-8')
    msgRoot.attach(msgText)
    #sendEmail
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()


# 检查网络连同性
def check_network():
    # 试验5次ping 百度，如果连通就返回True，否则返回False
    for i in range(0, 5):
        try:
            result=urllib.urlopen('http://baidu.com').read()
            #print result
            print "Network is Ready!"
            break
        except Exception , e:
            print e
            print "Network is not ready,Sleep 5s...."
            time.sleep(5)
    else:
        print "Sorry that pi isn't connectted to Internet now"
        return False
    return True


# 获得本级制定接口的ip地址
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1",80))
    ipaddr=s.getsockname()[0]
    s.close()
    return ipaddr


if __name__ == '__main__':
    if check_network():
        ipaddr = get_ip_address()
        now = datetime.datetime.now()
        time_info = now.strftime('%Y-%m-%d %A %H:%M:%S')
        send_text = "Boot time: %s\nIP addr: %s" % (time_info, ipaddr)
        sendEmail('smtp.163.com','raspi_robot@163.com','mangoer123','raspi_robot@163.com',['2395528746@qq.com'], 'Raspberry Pi boot status', send_text)
    else:
        print "Sorry that I can't help without network"