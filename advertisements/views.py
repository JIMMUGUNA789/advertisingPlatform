import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Ad
from companies.models import CompanyProfile
from django.contrib import messages

# INTEGRAION WITH MPESA API

import logging

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MpesaCheckoutSerializer
from .util import MpesaGateWay




def ad_click(request, ad_id):
    
    ad = get_object_or_404(Ad, pk=ad_id)
    ad.clicksCount += 1
    ad.save()
    company = ad.companyProfile.id
    return redirect(reverse('companyProfile', kwargs={'id':company}))

def show_ad(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    ad.impressionsCount += 1
    ad.save() 
    return ad.impressionsCount
def deleteAd(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    ad.delete()
    
    return redirect(reverse('adDashboard', kwargs={'user_id':request.user.id}))
def createAd(request, company_id):
    company_id = str(company_id)
    company = CompanyProfile.objects.get(id=company_id)
    if request.method == 'POST':
        
        companyProfile = company
        adImage = request.FILES['adImage']
        Ad_text = request.POST['Ad-text']
        adType = request.POST['adType']
        adStatus = 'Inactive'
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        # create the ad
        Ad.objects.create(companyProfile=companyProfile, adImage=adImage, Ad_text=Ad_text, adType=adType, adStatus=adStatus, startDate=startDate, endDate=endDate)
        messages.success(request, 'Ad created successfully')
        return redirect(reverse('adDashboard', kwargs={'user_id':request.user.id}))
        
    context = {
        "company": company,

    }
    return render(request, 'ads/createAd.html', context)


# INTEGRATION WITH MPESA API

gateway = MpesaGateWay()

@authentication_classes([])
@permission_classes((AllowAny,))
class MpesaCheckout(APIView):
    serializer = MpesaCheckoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payload = {"data":serializer.validated_data, "request":request}
            res = gateway.stk_push_request(payload)
            return Response(res, status=200)

@authentication_classes([])
@permission_classes((AllowAny,))
class MpesaCallBack(APIView):
    def get(self, request):
        return Response({"status": "OK"}, status=200)

    def post(self, request, *args, **kwargs):
        logging.info("{}".format("Callback from MPESA"))
        data = request.body
        return gateway.callback(json.loads(data))


