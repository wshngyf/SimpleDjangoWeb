from rest_framework import serializers
from LicensePlateManage.models import PhoneNum


class PhoneNumSerializers(serializers.ModelSerializer):
    class Meta:
        model=PhoneNum
        fields=('licenseplate','phoneNum','remark','author','createDate')