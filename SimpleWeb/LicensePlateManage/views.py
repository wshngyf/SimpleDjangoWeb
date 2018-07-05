from django.shortcuts import render
from django.http import HttpResponse
from LicensePlateManage.models import PhoneNum
from LicensePlateManage.serializer import PhoneNumSerializers
import time
import datetime
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from xlwt import *
import os
from io import BytesIO

def demo(request):
    return render(request, "demo.html")

def license(request):
    return render(request, "license.html")

def downloadexcel(request):
    return render(request,"download.html")

def licensejson(request):
    nowtime = datetime.datetime.now()
    #nowtime = timenow.strftime('%Y-%m-%d %H:%M:%S', timenow.localtime(timenow.time()))
    author=request.GET.get('author')
    plate=request.GET.get('plate')
    starttime=request.GET.get('starttime')
    endtime=request.GET.get('endtime')
    if not endtime =='':
        nowendtime= datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M")
    else:
        nowendtime=nowtime
    pageSize = int(request.GET.get('pageSize'))
    page=int(request.GET.get('page'))
    if page is None:
        page = 1
    if not author == '':
        licenseplate = PhoneNum.objects.filter(createDate__range=(starttime, nowendtime),author=author).order_by("-createDate")
    elif not plate =='':
        licenseplate = PhoneNum.objects.filter(licenseplate=plate).order_by("-createDate")
    elif not starttime =='':
        time = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M")
        licenseplate = PhoneNum.objects.filter(createDate__range=(starttime, nowendtime)).order_by("-createDate")
    else:
        licenseplate = PhoneNum.objects.all().order_by("-createDate")

    paginator = Paginator(licenseplate, pageSize)

    serializer = PhoneNumSerializers(paginator.page(page), many=True)

    con=serializer.data
    str=json.dumps({'rows': con,'page':page,'total':paginator.count})
    #return render(request, "index.html")
    #str={"rows": [{"province": "豫","city": "A","license": "00001","licenseplate": "豫A00001","phonenum": "13939112345","carnum": "2341243235345"}],"page": 1,"total": 1}
    return HttpResponse(str)
'''
def addData(request):
    data=LicensePlate(province='豫',city='A',license='00002',licenseplate='豫A00002',phonenum='123321123432',carnum='123134234234234')
    data.save()
    return HttpResponse("添加数据成功")
'''
#createDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
'''
def addTest(request):
    data=PhoneNum(province='豫',city='A',phoneNum='19937127339',carnum='00001',remark='',createDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    data.save()
    return HttpResponse("添加数据成功")
'''
def addLicense(request):
    province=request.GET.get('province')
    city=request.GET.get('city')
    phonenum=request.GET.get('phoneNum')
    carnum=request.GET.get('carnum')
    remark=request.GET.get('remark')
    author=request.GET.get('author')
    if province is None:
        return
    licenseplate=province + city + carnum
    try:
        PhoneNum.objects.get(licenseplate=licenseplate)
    except PhoneNum.DoesNotExist:
        data = PhoneNum(province=province, city=city, phoneNum=phonenum, carnum=carnum, licenseplate=licenseplate,
                        remark=remark,createDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                        author=author)
        data.save()
        str = json.dumps({'resultCode': 0, 'resultMessage': '添加成功', 'data': {'licenseplate': licenseplate, }})
        return HttpResponse(str)
    str = json.dumps({'resultCode': 100, 'resultMessage': '该号码已存在', 'data': {'licenseplate': licenseplate, }})
    return HttpResponse(str)


def saveExcel(request):
    nowtime = datetime.datetime.now()
    author = request.GET.get('author')
    starttime=request.GET.get('starttime')
    endtime=request.GET.get('endtime')
    if not endtime =='':
        nowendtime= datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M")
    else:
        nowendtime=nowtime
    if not starttime == '':
        time = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M")
        Licenseplate = PhoneNum.objects.filter(createDate__range=(time, nowendtime),author_contains=author).order_by("-createDate")
    else:
        Licenseplate = PhoneNum.objects.all().order_by("-createDate")
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

rows1=r'客户信息汇总'
rows2=r'确保业务员姓名和机器人系统业务员保持一致'
def saveExcelModel(request):
    nowtime = datetime.datetime.now()
    author = request.GET.get('author')
    time=request.GET.get('starttime')
    endtime=request.GET.get('endtime')
    if not endtime == '':
        nowendtime = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M")
    else:
        nowendtime = nowtime
    if not author=='':
        Licenseplate = PhoneNum.objects.filter(createDate__range=(time, nowendtime), author=author).order_by("-createDate")
    elif not time == '':
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        Licenseplate = PhoneNum.objects.filter(createDate__range=(time, nowendtime)).order_by("-createDate")
    else:
        Licenseplate = PhoneNum.objects.all().order_by("-createDate")
    if Licenseplate is None:
        return
    # 居中格式
    #alignment = Alignment()
    #alignment.horz = Alignment.HORZ_CENTER
    #alignment.vert = Alignment.VERT_CENTER
    #style2 = XFStyle()
    #style2.alignment=alignment

    # 日期格式
    #style1 = XFStyle()
    #style1.num_format_str = 'M/D/YY h:mm'
    #style1.alignment = alignment

    if Licenseplate:
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"上传模板")
        #w.write(0, 0, u"省份",style2)
        #w.write(0, 1, u"城市",style2)
        #w.write(0, 2, u"牌号",style2)
        #参数 1行 2跨行数 3列 4跨列数 5显示内容 6样式
        w.write_merge(0,0,0,12,rows1)
        w.write_merge(1,1,0,12,rows2)
        w.write(2, 0, u"车牌号")
        w.write(2, 1, u"车架号")
        w.write(2, 2, u"发动机号")
        w.write(2, 3, u"车主证件号码")
        w.write(2, 4, u"品牌型号")
        w.write(2, 5, u"注册日期")
        w.write(2, 6, u"去年投保公司")
        w.write(2, 7, u"交强险到期时间")
        w.write(2, 8, u"商业险到期时间")
        w.write(2, 9, u"客户姓名")
        w.write(2, 10, u"客户电话1")
        w.write(2, 11, u"客户电话2")
        w.write(2, 12, u"客户备注")
        w.write(2, 13, u"客户备注2")
        w.write(2, 14, u"客户类别")
        w.write(2, 15, u"业务员姓名")
        w.write(2, 16, u"业务员账号")

        w.col(0).width = 256 * 20
        w.col(1).width = 256 * 30
        w.col(2).width = 256 * 30
        w.col(3).width = 256 * 30
        w.col(4).width = 256 * 30
        w.col(5).width = 256 * 30
        w.col(6).width = 256 * 30
        w.col(7).width = 256 * 30
        w.col(8).width = 256 * 30
        w.col(9).width = 256 * 30
        w.col(10).width = 256 * 30
        w.col(11).width = 256 * 30
        w.col(12).width = 256 * 30
        w.col(13).width = 256 * 30
        w.col(14).width = 256 * 30
        w.col(15).width = 256 * 30
        w.col(16).width = 256 * 30
        # 写入数据
        excel_row = 3
        for obj in Licenseplate:
            data_remark = obj.remark
            data_province = obj.province
            data_city = obj.city
            data_carnum= obj.carnum
            data_licenseplate = obj.licenseplate
            dada_phonenum = obj.phoneNum
            data_author = obj.author
            data_createdate=obj.createDate
            #车牌号放到0列
            w.write(excel_row, 0, data_licenseplate)
            w.write(excel_row, 10, dada_phonenum)
            w.write(excel_row, 12, data_remark)
            w.write(excel_row, 15, data_author)
            #w.write(excel_row, 7, data_createdate,style1)
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
