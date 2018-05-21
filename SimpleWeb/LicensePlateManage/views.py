from django.shortcuts import render
from django.http import HttpResponse
from LicensePlateManage.models import LicensePlate
from LicensePlateManage.serializer import LicenseSerializers
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from xlwt import *
import os
from io import StringIO

def index(request):
    phone=request.GET.get('phone')
    plate=request.GET.get('plate')
    time=request.GET.get('time')
    pageSize = request.GET.get('pageSize')
    page=int(request.GET.get('offset'))
    if not phone=='':
        licenseplate = LicensePlate.objects.filter(phonenum=phone)
    elif not plate =='':
        licenseplate = LicensePlate.objects.filter(licenseplate=plate)
    elif not time =='':
        licenseplate = LicensePlate.objects.filter(startdate=time)
    else:
        licenseplate = LicensePlate.objects.all()

    paginator = Paginator(licenseplate, pageSize)
    page=page/5+1
    serializer = LicenseSerializers(paginator.page(page), many=True)

    con=serializer.data
    str=json.dumps({'rows': con,'page':page,'total':paginator.count})
    #return render(request, "index.html")
    #str={"rows": [{"province": "豫","city": "A","license": "00001","licenseplate": "豫A00001","phonenum": "13939112345","carnum": "2341243235345"}],"page": 1,"total": 1}
    return HttpResponse(str)

@login_required
def demo(request):
    return render(request, "demo.html")

def addData(request):
    data=LicensePlate(province='豫',city='A',license='00002',licenseplate='豫A00002',phonenum='123321123432',carnum='123134234234234')
    data.save()
    return HttpResponse("添加数据成功")

def downExcel(request):
    licenseplate = LicensePlate.objects.all()
    if licenseplate:
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"sheet1")
        w.write(0, 0, "车牌")
        w.write(0, 1, u"省份")
        w.write(0, 2, u"城市")
        w.write(0, 3, u"牌号")
        w.write(0, 4, u"手机号")
        # 写入数据
        excel_row = 1
        for obj in licenseplate:
            data_num = obj.carnum
            data_province = obj.province
            data_city = obj.city
            data_license = obj.license
            dada_phonenum = obj.phonenum
            w.write(excel_row, 0, data_num)
            w.write(excel_row, 1, data_province)
            w.write(excel_row, 2, data_city)
            w.write(excel_row, 3, data_license)
            w.write(excel_row, 4, dada_phonenum)
            excel_row += 1
            # 检测文件是够存在
        # 方框中代码是保存本地文件使用，如不需要请删除该代码
        ###########################
        exist_file = os.path.exists("test.xls")
        if exist_file:
            os.remove(r"test.xls")
        ws.save("test.xls")
        ############################
        #sio =StringIO.StringIO()
        #ws.save(sio)
        #sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=test.xls'
        #response.write(sio.getvalue())
        ws.save(response)
        return HttpResponse(response)

# Create your views here.
