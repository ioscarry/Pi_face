#!/usr/bin/python
#-*- coding:utf-8 -*-

import smtplib
from email import *
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

mail_host = 'smtp.mxhichina.com'
mail_user = 'facepi@wponder.xin'
mail_pass = 'PIface1024'

sender = 'facepi@wponder.xin'
receivers = 'lgx010330@foxmail.com'

msgRoot = MIMEMultipart('related')
msgRoot['From'] = Header("facepi@wponder.xin", 'utf-8')
msgRoot['To'] = Header('CUJAM',' utf-8')
subject = '有陌生人进入！！'
msgRoot['Subject'] = Header(subject, 'utf-8')

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)
mail_msg = """
<p>PI 已经获取了陌生人的图片</p>
<p>图片:</p>
<p><img src="cid:image1"></p>
"""
msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

fp = open('/home/pi/watchdog/Face/Face_Project/data/get_unknow/Known.jpg','rb')
msgImage = MIMEImage(fp.read())
fp.close()

msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, receivers, msgRoot.as_string())
#    print '邮件发送成功'
except smtplib.SMTPException:
    pass
#    print 'Error'
