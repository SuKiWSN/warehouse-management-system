from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import time
from foo.models import *

mail_host="smtp.qq.com"  #设置服务器
mail_user="27796554@qq.com"    #用户名
mail_pass="ypbisgnaqtbibgcd"   #口令
sender = '27796554@qq.com'
smtp = smtplib.SMTP_SSL("smtp.qq.com")
smtp.ehlo("smtp.qq.com")

def mail_code(request):
    list = user.objects.filter(userCode=request.POST.get('address'))
    if len(list):
        return JsonResponse({'status': 201, 'message': '账号已注册'})
    receiver = request.POST.get('address')
    receivers = [receiver]
    code = ''
    for _ in range(6):
        code += str(random.randint(1, 9))

    message = MIMEText("您的验证码是"+code+' 验证码5分钟内有效。请不要将此验证码告知他人', 'plain', 'utf-8')
    message['From'] = Header("欢迎注册仓库管理系统", 'utf-8')
    message['To'] = Header(receiver, 'utf-8')
    subject = '仓库管理系统验证码'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', port=465)
        smtpObj.connect(mail_host)#port=25
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        sql = vertifyCode(userCode=receiver, code=code, time=str(int(time.time())))
        sql.save()
        print('发送成功', code, receiver)
        return JsonResponse({'status': 200, 'message': '发送成功'})
    except smtplib.SMTPException:
        return JsonResponse({'status': 10024, 'message': '发送失败'})
