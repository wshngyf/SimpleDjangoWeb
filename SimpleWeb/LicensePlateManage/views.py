from django.shortcuts import render
from django.http import HttpResponse
from LicensePlateManage.models import LicensePlate
from LicensePlateManage.models import PhoneNum
from LicensePlateManage.serializer import LicenseSerializers,PhoneNumSerializers
import time
import datetime
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from xlwt import *
import os
from io import BytesIO
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

def demo(request):
    return render(request, "demo.html")

def license(request):
    return render(request, "license.html")

def downloadexcel(request):
    return render(request,"download.html")

def licensejson(request):
    nowtime = datetime.datetime.now()
    #nowtime = timenow.strftime('%Y-%m-%d %H:%M:%S', timenow.localtime(timenow.time()))
    phone=request.GET.get('phone')
    plate=request.GET.get('plate')
    time=request.GET.get('time')

    pageSize = int(request.GET.get('pageSize'))
    page=int(request.GET.get('offset'))
    if page is None:
        page=1
    if not phone=='':
        licenseplate = PhoneNum.objects.filter(phonenum=phone)
    elif not plate =='':
        licenseplate = PhoneNum.objects.filter(licenseplate=plate)
    elif not time =='':
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        licenseplate = PhoneNum.objects.filter(createDate__range=(time, nowtime))
    else:
        licenseplate = PhoneNum.objects.all()

    paginator = Paginator(licenseplate, pageSize)
    page=int(page/5+1)
    serializer = PhoneNumSerializers(paginator.page(page), many=True)

    con=serializer.data
    str=json.dumps({'rows': con,'page':page,'total':paginator.count})
    #return render(request, "index.html")
    #str={"rows": [{"province": "豫","city": "A","license": "00001","licenseplate": "豫A00001","phonenum": "13939112345","carnum": "2341243235345"}],"page": 1,"total": 1}
    return HttpResponse(str)

def addData(request):
    data=LicensePlate(province='豫',city='A',license='00002',licenseplate='豫A00002',phonenum='123321123432',carnum='123134234234234')
    data.save()
    return HttpResponse("添加数据成功")

#createDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
def addTest(request):
    data=PhoneNum(province='豫',city='A',phoneNum='19937127339',carnum='00001',remark='',createDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    data.save()
    return HttpResponse("添加数据成功")

def addLicense(request):
    province=request.GET.get('province')
    city=request.GET.get('city')
    phonenum=request.GET.get('phoneNum')
    carnum=request.GET.get('carnum')
    remark=request.GET.get('remark')
    author=request.GET.get('author')
    if province is None:
        return
    data=PhoneNum(province=province,city=city,phoneNum=phonenum,carnum=carnum,licenseplate=province+city+carnum,remark=remark,createDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),author=author)
    data.save()
    return HttpResponse("添加数据成功")

def saveExcel(request):
    nowtime = datetime.datetime.now()
    time=request.GET.get('starttime')
    if not time == '':
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        Licenseplate = PhoneNum.objects.filter(createDate__range=(time, nowtime))
    else:
        Licenseplate = PhoneNum.objects.all()
    if Licenseplate is None:
        return
    # 居中格式
    alignment = Alignment()
    alignment.horz = Alignment.HORZ_CENTER
    alignment.vert = Alignment.VERT_CENTER
    style2 = XFStyle()
    style2.alignment=alignment

    # 日期格式
    style1 = XFStyle()
    style1.num_format_str = 'M/D/YY h:mm'
    style1.alignment = alignment

    if Licenseplate:
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"sheet1")
        w.write(0, 0, u"省份",style2)
        w.write(0, 1, u"城市",style2)
        w.write(0, 2, u"牌号",style2)
        w.write(0, 3, u"车牌号",style2)
        w.write(0, 4, u"手机号",style2)
        w.write(0, 5, u"备注",style2)
        w.write(0, 6, u"采集人",style2)
        w.write(0, 7, u"添加时间",style1)
        w.col(4).width = 256 * 20
        w.col(5).width = 256 * 30
        w.col(7).width = 256 * 30
        # 写入数据
        excel_row = 1
        for obj in Licenseplate:
            data_remark = obj.remark
            data_province = obj.province
            data_city = obj.city
            data_carnum= obj.carnum
            data_licenseplate = obj.licenseplate
            dada_phonenum = obj.phoneNum
            data_author = obj.author
            data_createdate=obj.createDate
            w.write(excel_row, 0, data_province,style2)
            w.write(excel_row, 1, data_city,style2)
            w.write(excel_row, 2, data_carnum,style2)
            w.write(excel_row, 3, data_licenseplate,style2)
            w.write(excel_row, 4, dada_phonenum,style2)
            w.write(excel_row, 5, data_remark,style2)
            w.write(excel_row, 6, data_author,style2)
            w.write(excel_row, 7, data_createdate,style1)
            excel_row += 1
            # 检测文件是够存在
        # 方框中代码是保存本地文件使用，如不需要请删除该代码
        ###########################
        exist_file = os.path.exists(os.path.join('./static/file/test.xls'))
        if exist_file:
            os.remove(os.path.join('./static/file/test.xls'))
        ws.save("./static/file/test.xls")
        ############################
        '''
        sio =BytesIO()
        ws.save(sio)
        sio.seek(0)
        the_file_name = "test.xls"
        response = HttpResponse(sio.getvalue(),content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
        response.write(sio.getvalue())
        '''
        return HttpResponse("导出成功")

# Create your views here.
