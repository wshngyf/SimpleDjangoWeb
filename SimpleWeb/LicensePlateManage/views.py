from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from LicensePlateManage.models import LicensePlate
from LicensePlateManage.serializer import LicenseSerializers
import re
import json
import demjson

def index(request):
    licenseplate = LicensePlate.objects.all()
    serializer = LicenseSerializers(licenseplate, many=True)
    con=serializer.data
    str=json.dumps({'rows': con,'page':1,'total':20})
    #return render(request, "index.html")
    #str={"rows": [{"province": "豫","city": "A","license": "00001","licenseplate": "豫A00001","phonenum": "13939112345","carnum": "2341243235345"}],"page": 1,"total": 1}
    return HttpResponse(str)


def demo(request):
    return render(request, "demo.html")

def addData(request):
    data=LicensePlate(province='豫',city='A',license='00002',licenseplate='豫A00002',phonenum='123321123432',carnum='123134234234234')
    data.save()
    return HttpResponse("添加数据成功")


# Create your views here.
