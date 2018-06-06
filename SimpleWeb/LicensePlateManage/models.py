from django.db import models
import datetime

# Create your models here.

class PhoneNum(models.Model):
    licenseplate = models.CharField(max_length=10,unique=True,primary_key=True)
    phoneNum=models.CharField(max_length=11,default='无')
    province=models.CharField(max_length=12,default='无')
    city=models.CharField(max_length=12,default='无')
    carnum=models.CharField(max_length=8,default='0')
    author=models.CharField(max_length=10,default='无')
    remark=models.CharField(max_length=40,default='无')
    createDate=models.DateTimeField(null=True,default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

