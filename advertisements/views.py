from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Ad
from companies.models import CompanyProfile
from django.contrib import messages
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

    
