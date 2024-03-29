import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Ad
from companies.models import CompanyProfile
from django.contrib import messages

# INTEGRAION WITH MPESA API
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment
from datetime import datetime



# simulate a payment
import json
import requests
import os
from datetime import datetime as Date, timedelta

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pytz






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



def getAccessToken(request):
    consumer_key = 'wb8Sc8u5aCKrte0enX3fbq8VGLpggIOE'
    consumer_secret = 'a3nHWvTuoLGATd4r'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request, ad_id):
    ad_id = str(ad_id)
    
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254729825703,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254729825703,  # replace with your phone number to get stk push
        # "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "CallBackURL": "https://4781-154-159-237-135.in.ngrok.io/advertisements/c2b/confirmation/?ad_id="+ad_id,
        "AccountReference": "Digiverse",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')

@csrf_exempt
def register_urls(request):
    
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://4781-154-159-237-135.in.ngrok.io/advertisements/c2b/confirmation/?ad_id=",
               "ValidationURL": "https://4781-154-159-237-135.in.ngrok.io/advertisements/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt


def paymentConfirmation(request):
    print(request)
    mpesa_body =request.body.decode('utf-8')
    print(mpesa_body)
    print(request.GET.get('ad_id', None))

    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_payment)
    
    ad = Ad.objects.get(id=request.GET.get('ad_id', None))
    metadata = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item']
    amount = next(item for item in metadata if item['Name'] == 'Amount')['Value']
    receipt_number = next(item for item in metadata if item['Name'] == 'MpesaReceiptNumber')['Value']
    transaction_date_string = next(item for item in metadata if item['Name'] == 'TransactionDate')['Value']
    phone_number = next(item for item in metadata if item['Name'] == 'PhoneNumber')['Value']
    organization_balance = 1000
    date_format = "%Y%m%d%H%M%S"

    transaction_date = datetime.strptime(str(transaction_date_string), date_format)
    timezone = pytz.timezone("Africa/Nairobi")
    transaction_date = timezone.localize(transaction_date)

    payment = MpesaPayment.objects.create(
            ad_id=ad,
            amount=amount,
            phone_number=phone_number,
            mpesa_receipt_number=receipt_number,
            transaction_date=transaction_date,
            organization_balance=organization_balance,
            
        )

    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

# Simulate a payment

def simulate(request, ad_id):
    ad_id = str(ad_id)
    headers = {
        "Authorization": "Basic SWZPREdqdkdYM0FjWkFTcTdSa1RWZ2FTSklNY001RGQ6WUp4ZVcxMTZaV0dGNFIzaA=="
    }

    data = {'Body': {'stkCallback': {'MerchantRequestID': '4827-3022771-1', 'CheckoutRequestID': 'ws_CO_201020211417243449', 'ResultCode': 0, 'ResultDesc': 'The service request is processed successfully.', 'CallbackMetadata': {
        'Item': [{'Name': 'Amount', 'Value': 11100.0}, {'Name': 'MpesaReceiptNumber', 'Value': 'PJK9HS9EZP'}, {'Name': 'Balance'}, {'Name': 'TransactionDate', 'Value': 20220921141737}, {'Name': 'PhoneNumber', 'Value': 254729825703}]}}}}
    
    url = 'https://4781-154-159-237-135.in.ngrok.io/advertisements/c2b/confirmation/?ad_id='+ad_id
    requests.request("POST", url, json=data, headers=headers)
    
    
    print(data)
    
    return HttpResponse('success')

