import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import time
import os
import threading

mail_host="smtp.qq.com"  #设置服务器
mail_user="27796554@qq.com"    #用户名
mail_pass="ypbisgnaqtbibgcd"   #口令
sender = '27796554@qq.com'
smtp = smtplib.SMTP_SSL("smtp.qq.com")
smtp.ehlo("smtp.qq.com")

def sendmail():
    j = len(os.listdir('../image'))
    while 1:
        flnum = len(os.listdir('../image'))
        if flnum != j:
            receiver = '27796554@qq.com'
            receivers = [receiver]
            sendtime = str(datetime.datetime.now()).split('.')[0]
            message = MIMEText(f'您的仓库在{sendtime}检测到可疑物品移动。具体情况请登录仓库管理系统查看', 'plain', 'utf-8')
            message['From'] = Header("仓库报警提醒", 'utf-8')
            message['To'] = Header(receiver, 'utf-8')
            subject = '仓库管理系统报警'
            message['Subject'] = Header(subject, 'utf-8')
            try:
                smtpObj = smtplib.SMTP_SSL('smtp.qq.com', port=465)
                smtpObj.connect(mail_host)#port=25
                smtpObj.login(mail_user, mail_pass)
                smtpObj.sendmail(sender, receivers, message.as_string())
                print('发送成功', sendtime, receiver)
                time.sleep(1800)
                j = len(os.listdir('../image'))
            except:
                pass
        else:
            time.sleep(5)


if __name__ == '__main__':
    sendmail()