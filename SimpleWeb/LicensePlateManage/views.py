from django.shortcuts import render
from django.shortcuts import HttpResponse
from LicensePlateManage.models import LicensePlate
from LicensePlateManage.serializer import LicenseSerializers
import json
def index(request):
    licenseplate = LicensePlate.objects.all()
    serializer = LicenseSerializers(licenseplate, many=True)
    con=serializer.data
    #return render(request, "index.html")
    return HttpResponse(json.dumps({'allnum':con}),content_type="application/json")
# Create your views here.
