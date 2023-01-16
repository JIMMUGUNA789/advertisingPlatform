from django.shortcuts import render, redirect
from .models import CompanyProfile, Reviews, Likes, Follows 
from posts.models import Post
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.files.storage import default_storage



# Create your views here.
def home(request):
    companies = CompanyProfile.objects.all().order_by('?')
    context = {
        "companies":companies
    }
    
    return render(request, 'home.html', context)
    # company profile
def companyProfile(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)    
    posts = Post.objects.filter(company=id).order_by('-created_at')
    no_of_posts = Post.objects.filter(company=id).count()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        "company":company,
        "posts":page_obj,
        "no_of_posts":no_of_posts,
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

def addReview(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    if request.method == 'POST':
        company = company
        user = request.user
        rating = request.POST['rating']
        review = request.POST['review']
        reviewPhoto = request.FILES.get('reviewPhoto')
        review = Reviews.objects.create(company=company, user=user, rating=rating, review=review, reviewPhoto=reviewPhoto)
        review.save()
        messages.success(request, 'Review added successfully')
        return redirect('reviews', id=id)
    context = {
        "company":company,
    }
    return render(request, 'company/addReview.html', context)

def likeAndDislikeCompany(request, company_id):
    company =  CompanyProfile.objects.get(id=company_id)
    user = request.user
    if Likes.objects.filter(company=company, user=user).exists():
        Likes.objects.filter(company=company, user=user).delete()
        return redirect('companyProfile', id=company_id)
    else:
        like = Likes.objects.create(company=company, user=user)
        like.save()
        return redirect('companyProfile', id=company_id)
def followAndUnfollowCompany(request, company_id):
    company =  CompanyProfile.objects.get(id=company_id)
    user = request.user
    if Follows.objects.filter(company=company, user=user).exists():
        Follows.objects.filter(company=company, user=user).delete()
        return redirect('companyProfile', id=company_id)
    else:
        follow = Follows.objects.create(company=company, user=user)
        follow.save()
        return redirect('companyProfile', id=company_id)