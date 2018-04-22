from rest_framework import serializers
from LicensePlateManage.models import LicensePlate

class LicenseSerializers(serializers.ModelSerializer):
    class Meta:
        model=LicensePlate
        fields=('province','city','license','licenseplate','phonenum','carnum')
