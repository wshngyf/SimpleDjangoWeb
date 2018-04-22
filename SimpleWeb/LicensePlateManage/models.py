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

