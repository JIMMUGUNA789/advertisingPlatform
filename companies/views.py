from django.shortcuts import render, redirect
from .models import CompanyProfile, Reviews
from posts.models import Post
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.files.storage import default_storage



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
    posts = Post.objects.filter(company=id).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "company":company,
        "posts":page_obj,
    }
    return render(request, 'company/companyProfile.html', context)

def companyPhotos(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id).order_by('-created_at')
    context = {
        "company":company,
        "posts":posts,
    }
    return render(request, 'company/photos.html', context)

def reviews(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    reviews = Reviews.objects.filter(company=id).order_by('-created_at')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "reviews":page_obj,
        "company":company,
    }
    return render(request, 'company/reviews.html', context)

def listCompany(request):
    if request.method == 'POST':
        companyName = request.POST['companyName']
        companyAdmin = request.user
        description = request.POST['description']
        profilePicture = request.FILES.get('profilePicture')      
        bannerPicture = request.FILES.get('bannerPicture')
        category = request.POST.get('category')
        phone = request.POST['phone']
        email = request.POST['email']
        websiteUrl = request.POST['websiteUrl']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        address = request.POST['address']        
        companyProfile = CompanyProfile(companyName=companyName, companyAdmin=companyAdmin, description=description, profilePicture=profilePicture, bannerPicture=bannerPicture, category=category, phone=phone, email=email, websiteUrl=websiteUrl, latitude=latitude, longitude=longitude, address=address)
        companyProfile.save()
      
        messages.success(request, 'Company profile created successfully')
        # redirect to the company profile page
        return redirect('companyProfile', id=companyProfile.id)
        
    
    return render(request, 'company/listCompany.html')