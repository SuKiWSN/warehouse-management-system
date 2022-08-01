from django.http import HttpResponse
import datetime
import pytz
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world!")

def test(request):
    context = {}
    time = datetime.datetime.now()
    context['time'] = time
    context['hello'] = 'hello World!'
    context['name'] = "I love Wangshengnan"
    context['a_href'] = '<a href="https://www.baidu.com">点击跳转</a>'
    return render(request, 'test.html', context)