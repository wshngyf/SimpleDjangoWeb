from django.shortcuts import render
from django.http import HttpResponse
from LicensePlateManage.models import LicensePlate
from LicensePlateManage.serializer import LicenseSerializers
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    licenseplate = LicensePlate.objects.all()
    pageSize = request.GET.get('pageSize')
    page=int(request.GET.get('offset'))
    paginator = Paginator(licenseplate, pageSize)
    page=page/5+1
    serializer = LicenseSerializers(paginator.page(page), many=True)

    con=serializer.data
    str=json.dumps({'rows': con,'page':page,'total':paginator.count})
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
