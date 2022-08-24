from django.http import HttpResponse, JsonResponse
import datetime
import time
from django.shortcuts import render, redirect
from foo.models import *
import django.db.utils
import base64
import os

def manage(request):
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    if not usr or not pwd:
        return render(request, 'test.html')
    a = user.objects.filter(userCode=usr)[0]
    if a.userRole == 1 and pwd == a.userPassword:
        content = {}
        content['userCode'] = a.userCode
        content['userName'] = a.userName
        content['userPassword'] = a.userPassword
        content['phone'] = a.phone
        content['address'] = a.address
        d = datetime.date.today()
        b = a.birthday
        if b != None:
            age = d.year - b.year - int((d.month, d.day) < (b.month, b.day))
        else:
            age = ''
        content['userAge'] = age
        content['creationDate'] = a.creationDate
        content['userRole'] = a.userRole
        content['gender'] = a.gender
        return render(request, 'manage.html', content)
    else:
        return HttpResponse('用户权限不足')

def get_user(request):
    content = {}
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    if not usr or not pwd:
        return redirect('/test')

    else:
        list = user.objects.filter(userCode=usr)
        if len(list):
            a = list[0]
            if pwd == a.userPassword:
                content['userCode'] = a.userCode
                content['userName'] = a.userName
                content['userPassword'] = a.userPassword
                content['phone'] = a.phone
                content['address'] = a.address
                d = datetime.date.today()
                b = a.birthday
                if a.birthday != '' and a.birthday != None:
                    age = d.year - b.year - int((d.month, d.day) < (b.month, b.day))
                else:
                    age = ''
                content['userAge'] = age
                content['creationDate'] = a.creationDate
                content['userRole'] = a.userRole
                content['gender'] = a.gender
                return render(request, 'usrmessage.html', content)
            else:
                return redirect('/test')
        else:
            return redirect('/test')

def modify(request):
    name = request.POST.get('name')
    gender = request.POST.get('gend')

    address = request.POST.get('address').split('：')[-1].split('\n')[0]
    a = user.objects.filter(userCode=address)[0]
    a.name = name
    a.gend = gender
    a.save()
    return JsonResponse({'code': 200, 'message': "success"})

def changegender(request):
    userCode = request.POST.get('usr')
    a = user.objects.filter(userCode=userCode)[0]
    gender = a.gender
    a.gender = 3-gender
    a.save()
    return JsonResponse({'code': 200, 'message': "success"})

def changepwd(request):
    userCode = request.POST.get('address')
    pwd = request.POST.get('pwd')
    a = user.objects.filter(userCode=userCode)[0]
    a.userPassword = pwd
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def changeage(request):
    userCode = request.POST.get('usr')
    age = request.POST.get('age')
    age = datetime.datetime.strptime(age, '%Y-%m-%d').date()
    a = user.objects.filter(userCode=userCode)[0]
    a.birthday = age
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def addbill(request):
    usr = request.POST.get('usr')
    a = user.objects.filter(userCode=usr)[0]
    cid = a.id
    billCode = request.POST.get('billCode')
    billName = request.POST.get('billName')
    billDesc = request.POST.get('billDesc')
    billUnit = request.POST.get('billUnit')
    billCount = float(request.POST.get('billCount'))
    billPrice = float(request.POST.get('billPrice'))
    billProvider = int(request.POST.get("billProvider"))
    newbill = bill(billCode=billCode, productName=billName, productDesc=billDesc, productUnit=billUnit, productCount=billCount, totalPrice=billPrice, providerId=billProvider, createdBy=cid)
    newbill.save()
    return JsonResponse({"code": 200, 'message': 'success'})

def getpicture(request):
    id = request.POST.get('id')
    imgPath = alarm.objects.filter(id=id)[0].imgPath
    f = open(imgPath, 'rb')
    data = f.read()
    return JsonResponse({'code': 200, 'data': base64.b64encode(data).decode('ascii')})

def getdetail(request):
    id = request.POST.get('id')
    img = alarm.objects.filter(id=id)[0]
    imgPath = img.imgPath
    alarmCode = img.alarmCode
    deviceCode = img.deviceCode
    deviceName = img.deviceName
    alarmDate = img.alarmDate
    alarmType = img.alarmType
    processDate = img.processDate
    processState = img.processState
    processResult = img.processResult
    processor = img.processor
    processor = user.objects.filter(userCode=processor)[0].userName
    remarks = img.remarks
    if remarks == None:
        remarks = ''
    f = open(imgPath, 'rb')
    data = f.read()
    return JsonResponse({'code': 200, 'content': [alarmCode, deviceCode, deviceName, alarmDate, alarmType, processDate, processState, processResult, processor, remarks], 'data': base64.b64encode(data).decode('ascii')})

def getrole(request):
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    a = user.objects.filter(userCode=usr)[0]
    if pwd != a.userPassword:
        return JsonResponse({'code': 10024, 'message': 'incorrect password'})

    else:
        lis = role.objects.filter().order_by('id')
        content = []
        for var in lis:
            content.append([var.id, var.roleCode, var.roleName, var.createdBy, var.creationDate])
        return JsonResponse({'code': 200, 'content': content})

def mdfrole(request):
    id = request.POST.get('id')
    data = request.POST.get('data')
    type = request.POST.get('type')
    a = role.objects.filter(id=id)[0]
    try:
        if type == '1':
            a.roleCode = data
        elif type == '2':
            a.roleName = data
        a.save()
        return JsonResponse({'code': 200, 'message': '修改成功'})
    except django.db.utils.DataError:
        return JsonResponse({'code': 10024, 'message': '字符过长'})

def deleterole(request):
    usr = request.POST.get('userCode')
    pwd = request.POST.get('pwd')
    a = user.objects.filter(userCode=usr)[0]
    if a.userPassword == pwd:
        roleId = request.POST.get('roleId')
        if roleId == '1':
            return JsonResponse({'code': 10023, 'message': '系统管理员无法删除'})
        users = user.objects.filter()
        for var in users:
            if int(roleId) == var.userRole:
                return JsonResponse({'code': 10025, 'message': 'role is not null'})
        b = role.objects.filter(id=roleId)[0]
        b.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    else:
        return JsonResponse({'code': 10024, 'message': 'incorrect password'})

def addrole(request):
    userCode = request.POST.get('userCode')
    pwd = request.POST.get('userPassword')
    a = user.objects.filter(userCode=userCode)[0]
    createdBy = a.id
    if a.userPassword == pwd:
        roleCode = request.POST.get('roleCode')
        roleName = request.POST.get('roleName')
        b = role(roleCode=roleCode, roleName=roleName, createdBy=createdBy)
        b.save()
        return JsonResponse({'code': 200, 'message': 'success'})
    else:
        return JsonResponse({'code': 10024, 'message': 'incorrect password'})

def change(request):
    userCode = request.POST.get('usr')
    data = request.POST.get('data')
    type = request.POST.get('type')
    a = user.objects.filter(userCode=userCode)[0]
    if type == '1':
        a.userName = data
    elif type == '2':
        a.address = data
    elif type == '3':
        a.phone = data
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

# def user_role(request):
#     pwd = request.POST.get('pwd')
#     usr = request.POST.get('usr')
#     list = user.objects.filter(userCode=usr)[0]
#     role = list.role
#     return JsonResponse({'code': 10024, 'message': role})

def getusers(request):
    userCode = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    a = user.objects.filter(userCode=userCode)[0]
    content = []
    if pwd == a.userPassword:
        userRole = a.userRole
        if userRole == 1:
            list = user.objects.filter().all()
            for var in list:
                d = datetime.date.today()
                b = var.birthday
                if b != '' and b != None:
                    age = d.year - b.year - int((d.month, d.day) < (b.month, b.day))
                else:
                    age = ''
                content.append([var.userCode, var.userName, age, var.phone, var.userPassword, var.address, var.gender, var.userRole, var.department])
                if var.userRole == 1 and var.userCode != a.userCode:
                    content[-1][4] = '********'

            rolelists = role.objects.filter()
            rolelist = []
            deptlists = department.objects.filter()
            deptlist = []

            for roles in rolelists:
                rolelist.append([roles.roleName, roles.id])
            for depts in deptlists:
                deptlist.append([depts.departName, depts.id])
            return JsonResponse({'message': 'pass', 'content': content, 'rolelist': rolelist, 'deptlist': deptlist})
        else:
            return JsonResponse({'message': 'notpass', 'content':content})
    else:
        return JsonResponse({'message': 'notpass', 'content': content})

def search_usr_by_params(param, searchfor, manager, dept):
    content = []
    if param == 'userCode':
        list = user.objects.filter(userCode__contains=searchfor)
    elif param == 'userName':
        list = user.objects.filter(userName__contains=searchfor)
    elif param == 'userPassword':
        list = user.objects.filter(userPassword__contains=searchfor)
    elif param == 'phone':
        list = user.objects.filter(phone__contains=searchfor)
    elif param == 'address':
        list = user.objects.filter(address__contains=searchfor)
    else:
        list = None

    if dept != '0':
        list = list.filter(department=dept)
    for var in list:
        if param == 'userPassword' and var.userCode != manager.userCode and var.userRole == 1:
            continue
        d = datetime.date.today()
        b = var.birthday
        if b != '' and b != None:
            age = d.year - b.year - int((d.month, d.day) < (b.month, b.day))
        else:
            age = ''
        content.append(
            [var.userCode, var.userName, age, var.phone, var.userPassword, var.address, var.gender, var.userRole, var.department])
        if var.userRole == 1 and var.userCode != manager.userCode:
            content[-1][4] = '********'
    return content

def search_usr(request):
    searchfor = request.POST.get('usr')
    usr = request.POST.get('address')
    dept = request.POST.get('dept')

    a = user.objects.filter(userCode=usr)[0]
    content = []
    params = ['userCode', 'userName', 'userPassword', 'phone', 'address']
    for param in params:
        for var in search_usr_by_params(param, searchfor, a, dept):
            f = 0
            for i in content:
                if i[0] == var[0]:
                    f = 1
                    break
            if f == 0:
                content.append(var)
    deptlists = department.objects.filter()
    deptlist = []
    for depts in deptlists:
        deptlist.append([depts.departName, depts.id])

    rolelists = role.objects.filter()
    rolelist = []
    for roles in rolelists:
        rolelist.append([roles.roleName, roles.id])
    return JsonResponse({'content': content, 'deptlist': deptlist, 'rolelist': rolelist})

def add_user(request):
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    if len(user.objects.filter(userCode=usr)):
        return JsonResponse({'message': 'exists'})
    elif usr == '' or usr == None or pwd == '' or pwd == None:
        return JsonResponse({'message': 'null value'})
    userName = request.POST.get('userName')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    gender = request.POST.get('gender')

    a = user(userCode=usr, userName=userName, userPassword=pwd, phone=phone, address=address, gender=gender)
    a.save()
    return JsonResponse({'message': "succeed"})

def deleteusr(request):
    usr = request.POST.get('usr')
    address = request.POST.get('address')
    password = request.POST.get('pwd')
    manager = user.objects.filter(userCode=address)[0]
    role = manager.userRole
    list = user.objects.filter(userCode=usr)
    if len(list):
        if list[0].userRole == 3 or list[0].userRole == 2:
            list[0].delete()
            return JsonResponse({'code': 200, 'message': 'success'})
        elif usr == address:
            return JsonResponse({'code': 10022, 'message': 'can not delete self'})
        elif list[0].userRole == 1 and role == 1:
            return JsonResponse({'code': 10023, 'message': 'power error'})
    else:
        return JsonResponse({'code': 10024, 'message': 'fault'})

def mdfbill(requtst):
    id = requtst.POST.get('id')
    data = requtst.POST.get('data')
    type = requtst.POST.get('type')
    a = bill.objects.filter(id=id)[0]
    if type == '2':
        a.productName = data
    elif type == '3':
        a.productDesc = data
    elif type == '4':
        a.productUnit = data
    elif type == '5':
        a.productCount = int(data)
    elif type == '6':
        a.totalPrice = float(data)
    elif type == '8':
        a.providerId = int(data)
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def inmoney(request):
    usr = request.POST.get('usr')
    money = request.POST.get('money')
    name = request.POST.get('name')
    var = clients.objects.filter(address=usr)[0]
    try:
    	var.assets += int(money)
    	var.save()
    	rechargerecord(usr, name, int(money))
    	return JsonResponse({'message': 'success'})
    except:
    	return JsonResponse({'message': 'moneyerror'})

def getdepartment(request):
    userCode = request.POST.get('userCode')
    userPassword = request.POST.get('userPassword')
    a = user.objects.filter(userCode=userCode)[0]
    if a.userPassword == userPassword:
        dptlist = department.objects.filter()
        content = []
        for dpt in dptlist:
            content.append([dpt.id, dpt.departCode, dpt.departName, dpt.memberNum, dpt.departManager, dpt.departPhone])
        return JsonResponse({'code': 200, 'content': content})
    else:
        return JsonResponse({'code': 10024, 'message': 'incorrect password'})

def mdfdept(request):
    id = request.POST.get('id')
    type = int(request.POST.get('type'))
    data = request.POST.get('data')
    a = department.objects.filter(id=id)[0]
    if type == 1:
        a.departCode = data
    elif type == 2:
        a.departName = data
    elif type == 4:
        a.departManager = data
    elif type == 5:
        a.departPhone = data
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def deletedept(request):
    deptId = int(request.POST.get('deptId'))
    userCode = request.POST.get('userCode')
    pwd = request.POST.get('pwd')
    a = user.objects.filter(userCode=userCode)[0]
    if a.userPassword == pwd:
        userlist = user.objects.filter(department=deptId)
        if len(userlist):
            return JsonResponse({'code': 10024, 'message': 'error'})

        b = department.objects.filter(id=deptId)[0]
        b.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    else:
        return JsonResponse({'code': 404, 'message': 'error'})

def adddept(request):
    deptCode = request.POST.get('deptCode')
    deptName = request.POST.get('deptName')
    deptManager = request.POST.get('deptManager')
    deptPhone = request.POST.get('deptPhone')
    a = department(departName=deptName, departCode=deptCode, departManager=deptManager, departPhone=deptPhone, memberNum=0)
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def get_Rechargerecord(request):
    ty = request.POST.get('type')
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    a = user.objects.filter(userCode=usr)[0]
    if pwd == a.userPassword:
        content = []
        list = bill.objects.filter().all().order_by('-creationDate')
        if ty == '0':
            start = 0
            end = time.time()
        elif ty == '1':
            passed = (time.time() + 8 * 60 * 60) %(60*60*24)
            start = time.time() - passed
            end = time.time()
        elif ty == '2':
            passed = (time.time() + (3 * 60 * 60 * 24) + 8 * 60 * 60) % (60 * 60 * 24 * 7)
            start = time.time() - passed
            end = time.time()
        else:
            a = time.time()
            b = time.localtime(a)
            c = time.strftime('%d', b)
            c = int(c) - 1
            passed = c * 60 * 60 * 24 + (time.time() + 8 * 60 * 60) % (60*60*24)
            start = time.time() - passed
            end = time.time()
        sum = 0
        for var in list:
            creationdate = var.creationDate
            date = int(time.mktime(creationdate.timetuple()) * 1000.0 + creationdate.microsecond / 1000.0)/1000

            if date > start and date < end:
                sum += var.totalPrice
                content.append([var.id, var.billCode, var.productName, var.productDesc, var.productUnit, var.productCount, var.totalPrice, var.creationDate, var.providerId])

        return JsonResponse({'message': 'success', 'content': content, 'sum': sum})

    else:
        return JsonResponse({'message': 'error'})

def deletebill(request):
    userCode = request.POST.get('userCode')
    userPassword = request.POST.get('pwd')
    billId = request.POST.get('billId')
    a = user.objects.filter(userCode=userCode)[0]
    if userPassword == a.userPassword:
        b = bill.objects.filter(id=billId)[0]
        b.delete()
        return JsonResponse({'code': 200, 'message': 'success'})
    else:
        return JsonResponse({'code': 10024, 'message': 'password incorrect'})



def changerole(request):
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    address = request.POST.get('address')
    af_role = int(request.POST.get('af_role'))
    changer = user.objects.filter(userCode=usr)[0]
    userCode = changer.userCode
    if userCode != 'admin':
        return JsonResponse({'code': 10024, 'message': 'no power'})
    else:
        if usr == address:
            return JsonResponse({'code': 10023, 'message': 'can not change root power'})
        else:
            be_changed = user.objects.filter(userCode=address)[0]
            be_changed.userRole = af_role
            be_changed.save()
            return JsonResponse({'code': 200, 'message': 'success'})

def changedept(request):
    # usr = request.POST.get('usr')
    # pwd = request.POST.get('pwd')
    address = request.POST.get('address')
    af_dept = int(request.POST.get('af_dept'))
    be_changed = user.objects.filter(userCode=address)[0]
    bf_dept = be_changed.department
    if bf_dept != None and bf_dept != '':
        b = department.objects.filter(id=bf_dept)[0]
        b.memberNum -= 1
        b.save()
    c = department.objects.filter(id=af_dept)[0]
    c.memberNum += 1
    c.save()

    be_changed.department = af_dept
    be_changed.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def getalarm(request):
    type = int(request.POST.get('type'))
    list = alarm.objects.filter()
    page = int(request.POST.get('page'))
    start = (page-1)*10
    end = start + 10
    content = []
    if type == 1:
        list = list.filter(processState=0)
    elif type == 2:
        list = list.filter(processState=1)
    elif type == 3:
        list = list.filter(processResult=0)
    elif type == 4:
        list = list.filter(processResult=1)


    pages = len(list)
    if pages % 10 == 0:
        pages = pages // 10
    else:
        pages = pages // 10 + 1

    if pages == 0:
        pages = 1
    list = list[start: end]

    for var in list:
        content.append([var.id, var.alarmCode, var.deviceCode, var.deviceName, var.alarmDate, var.alarmType])
    return JsonResponse({'code': 200, 'message': 'success', 'content': content, 'pages': pages})

def processalarm(request):
    id = request.POST.get('id')
    ty = int(request.POST.get('type'))
    userCode = request.POST.get('usr')
    remarks = request.POST.get('remarks')
    print(remarks, id)
    a = alarm.objects.filter(id=id)[0]
    a.processState = 1
    a.processDate = datetime.datetime.now()
    a.processor = userCode
    a.remarks = remarks
    if ty == 0:
        a.processResult = 0
    elif ty == 1:
        a.processResult = 1
    a.save()
    return JsonResponse({'code': 200, 'message': 'success'})

def deletealarm(request):
    id = request.POST.get('id')

    al = alarm.objects.filter(id=id)[0]
    imgPath = al.imgPath
    os.remove(imgPath)
    al.delete()
    return JsonResponse({'code': 200, 'message': 'success'})

def multiop(request):
    type = int(request.POST.get('type'))
    li = request.POST.getlist('list')
    usr = request.POST.get('usr')
    print(type, li)
    if not(type == 1 or type == 2 or type == 3):
        return JsonResponse({'code': 400, 'message': 'error'})
    for i in li:
        a = alarm.objects.filter(id=int(i))[0]
        if type == 1:
            os.remove(a.imgPath)
            a.delete()
        elif type == 2:
            a.processState = 1
            a.processDate = datetime.datetime.now()
            a.processResult = 0
            a.processor = usr
            a.remarks = "批量处理"
            a.save()
        elif type == 3:
            a.processState = 1
            a.processDate = datetime.datetime.now()
            a.processResult = 1
            a.processor = usr
            a.remarks = "批量处理"
            a.save()
    return JsonResponse({'code': 200, 'message': 'success'})