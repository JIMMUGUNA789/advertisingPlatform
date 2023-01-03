from django.shortcuts import render
from .models import CompanyProfile

# Create your views here.
def home(request):
    companies = CompanyProfile.objects.all()
    context = {
        "companies":companies
    }
    
    return render(request, 'home.html', context)
def companyProfile(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    context = {
        "company":company
    }
    return render(request, 'company/companyProfile.html', context)
