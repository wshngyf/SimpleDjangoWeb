from django.db import models

# Create your models here.
class LicensePlate(models.Model):
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    license = models.CharField(max_length=5)
    licenseplate = models.CharField(max_length=10)
    phonenum = models.CharField(max_length=11)
    carnum = models.CharField(max_length=30)
    startdate = models.DateField(null=True)

class PhoneNum(models.Model):
    province=models.CharField(max_length=10)
    carnum=models.CharField(max_length=8,default='0')
    city=models.CharField(max_length=10)
    licenseplate = models.CharField(max_length=10,default='')
    phoneNum=models.CharField(max_length=13)
    license=models.CharField(max_length=10,default='')
    remark=models.CharField(max_length=40,default='无')
    author=models.CharField(max_length=10,default='无')
    createDate=models.DateTimeField(null=True,default='')

