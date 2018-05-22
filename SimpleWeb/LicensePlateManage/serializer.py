from rest_framework import serializers
from LicensePlateManage.models import LicensePlate
from LicensePlateManage.models import PhoneNum

class LicenseSerializers(serializers.ModelSerializer):
    class Meta:
        model=LicensePlate
        fields=('province','city','license','licenseplate','phonenum','carnum',)

class PhoneNumSerializers(serializers.ModelSerializer):
    class Meta:
        model=PhoneNum
        fields=('province','city','carnum','licenseplate','phoneNum','remark','author')