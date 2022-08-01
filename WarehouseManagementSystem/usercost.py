from django.http import HttpResponse, JsonResponse
import datetime
import time
from django.shortcuts import render, redirect
# from testmodel.models import vertify, clients, recharge, usr_cost

def user_spend(request):
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    spend = float(request.POST.get('spend'))
    ty = request.POST.get('type')
    b = clients.objects.filter(address=usr)[0]
    print(usr, pwd, spend, ty)
    print(type(usr), type(pwd), type(spend), type(ty))
    if pwd == b.password:
        if ty == '1':
            if spend > 0:
                usr_cost(address=usr, name=b.name, cost=spend, date=time.time()).save()
                if b.assets < spend:
                    spend = b.assets
                b.assets -= spend
                b.save()
                return JsonResponse({'code': 200, 'message': 'success'})
            else:
                return JsonResponse({'code': 10024, 'message': 'Parameter error!'})
        elif ty == '0':
            if spend > 0:
                sub = b.assets - spend
                if sub > 0:
                    return JsonResponse({'code': 200, 'message': 'continue'})
                else:
                    return JsonResponse({'code': 201, 'message': 'no_money'})
    else:
        return JsonResponse({'code': 10024, 'message': 'Password error!'})

def consume_record(request):
    li = usr_cost.objects.filter()
    for var in li:
        try:
            s = clients.objects.filter(address=var.address)[0]
            var.name = s.name
            var.save()
        except:
            pass
    usr = request.POST.get('usr')
    pwd = request.POST.get('pwd')
    ty = request.POST.get('type')
    b = clients.objects.filter(address=usr)[0]
    if pwd == b.password:
        content = []
        list = usr_cost.objects.filter().all().order_by('-date')
        if ty == '0':
            start = 0
            end = time.time()
        elif ty == '1':
            passed = time.time() % (60 * 60 * 24) + 8 * 60 * 60
            start = time.time() - passed
            end = time.time()
        elif ty == '2':
            passed = time.time() % (60 * 60 * 24 * 7) + (3 * 60 * 60 * 24) + 8 * 60 * 60  # 1970.1.1 是周四,要加3天
            start = time.time() - passed
            end = time.time()
        else:
            a = time.time()
            b = time.localtime(a)
            c = time.strftime('%d', b)
            c = int(c) - 1
            passed = c * 60 * 60 * 24 * c + time.time() % (60 * 60 * 24) + 8 * 60 * 60
            start = time.time() - passed
            end = time.time()
        sum = 0
        for var in list:
            if var.date > start and var.date < end:
                sum += var.cost
                array = time.localtime(var.date)
                date = time.strftime("%Y-%m-%d %H:%M:%S", array)
                content.append([var.address, var.name, var.cost, date])

        return JsonResponse({'message': 'success', 'content': content, 'sum': sum})

    else:
        return JsonResponse({'message': 'error'})
