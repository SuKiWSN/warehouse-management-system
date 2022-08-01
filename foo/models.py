from django.db import models

# Create your models here.
class address(models.Model):
    contact = models.CharField(max_length=15)
    addressDesc = models.CharField(max_length=50)
    postCode = models.CharField(max_length=15)
    tel = models.CharField(max_length=20)
    createdBy = models.BigIntegerField()
    creationDate = models.DateTimeField()
    modifyBy = models.BigIntegerField()
    modifyDate = models.DateTimeField()
    userId = models.BigIntegerField()

class bill(models.Model):
    billCode = models.CharField(max_length=20)
    productName = models.CharField(max_length=20)
    productDesc = models.CharField(max_length=50)
    productUnit = models.CharField(max_length=10)
    productCount = models.DecimalField(max_digits=20, decimal_places=2)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=2)
    isPayment = models.IntegerField(null=True)
    createdBy = models.BigIntegerField()
    creationDate = models.DateTimeField(auto_now=True)
    modifyBy = models.BigIntegerField(null=True)
    modifyDate = models.DateTimeField(null=True)
    providerId = models.BigIntegerField()

class provider(models.Model):
    proCode = models.CharField(max_length=20)
    proName = models.CharField(max_length=20)
    proDesc = models.CharField(max_length=50)
    proContact = models.CharField(max_length=20)
    proPhone = models.CharField(max_length=20)
    proAddress = models.CharField(max_length=50)
    proFax = models.CharField(max_length=20)
    createdBy = models.BigIntegerField()
    creationDate = models.DateTimeField()
    modifyDate = models.DateTimeField()
    modifyBy = models.BigIntegerField()

class role(models.Model):
    roleCode = models.CharField(max_length=15)
    roleName = models.CharField(max_length=15)
    createdBy = models.BigIntegerField()
    creationDate = models.DateTimeField(auto_now=True)
    modifyBy = models.BigIntegerField()
    modifyDate = models.DateTimeField()

class user(models.Model):
    userCode = models.CharField(max_length=20)
    userName = models.CharField(max_length=20, null=True)
    userPassword = models.CharField(max_length=15)
    gender = models.IntegerField(default=1)
    birthday = models.DateTimeField(null=True)
    department = models.IntegerField(null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=30, null=True)
    userRole = models.BigIntegerField(default=3)
    createdBy = models.BigIntegerField(default=1)
    creationDate = models.DateTimeField(auto_now=True)
    modifyBy = models.BigIntegerField(null=True)
    modifyDate = models.DateTimeField(null=True)
    idPicPath = models.CharField(max_length=200, null=True)
    workPicPath = models.CharField(max_length=200, null=True)

class vertifyCode(models.Model):
    userCode = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    time = models.IntegerField()

class department(models.Model):
    departCode = models.CharField(max_length=15)
    departName=models.CharField(max_length=10)
    memberNum=models.BigIntegerField()
    departManager=models.CharField(max_length=10)
    departPhone = models.CharField(max_length=20)
    createdBy = models.BigIntegerField(default=1)
    creationDate = models.DateTimeField(auto_now=True)
    modifyBy = models.BigIntegerField(null=True)
    modifyDate = models.DateTimeField(null=True)

class alarm(models.Model):
    alarmCode =models.CharField(max_length=15)#报警编号
    deviceCode =models.CharField(max_length=15)#设备编号
    deviceName =models.CharField(max_length=20)#设备名称
    alarmDate = models.DateTimeField(auto_now=False)#报警日期
    alarmType=models.CharField(max_length=15)#报警类型
    processDate =models.DateTimeField(null=True)#处理时间
    processState = models.BooleanField()
    processResult = models.IntegerField(null=True)
    processor = models.CharField(max_length=20, null=True)
    imgPath=models.CharField(max_length=150)
