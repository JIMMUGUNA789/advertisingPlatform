from django.shortcuts import render
from .models import CompanyProfile
from posts.models import Post

# Create your views here.
def home(request):
    companies = CompanyProfile.objects.all()
    context = {
        "companies":companies
    }
    
    return render(request, 'home.html', context)
    # company profile
def companyProfile(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    
    context = {
        "company":company,
        "posts":posts,
    }
    return render(request, 'company/companyProfile.html', context)

def companyPhotos(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    context = {
        "company":company,
        "posts":posts,
    }
    return render(request, 'company/photos.html', context)