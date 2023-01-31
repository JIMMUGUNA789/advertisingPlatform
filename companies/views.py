from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy


from .models import CompanyProfile, Reviews, Likes, Follows, CompanyImages
from posts.models import Post, PostComments
from django.core.paginator import Paginator
from django.contrib import messages
from ads.models import Advertiser
from django.db.models.functions import Random

from django.core.files.storage import default_storage
from django.views.generic.edit import UpdateView
from django.db.models import Avg




# Create your views here.
def home(request):
    companies = CompanyProfile.objects.all().order_by('?')
    for company in companies:
        avg_rating = Reviews.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']
        company.avg_rating = avg_rating
        
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
    # get the average rating of the company
    avg_rating = Reviews.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']

    
    
    context = {
        "company":company,
        "posts":page_obj,
        "no_of_posts":no_of_posts,
        "avg_rating":avg_rating
    }
    return render(request, 'company/companyProfile.html', context)

def companyPhotos(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id).order_by('?')
    images = CompanyImages.objects.filter(company=id).order_by('?')
    avg_rating = Reviews.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']
    print(images)
    context = {
        "company":company,
        "posts":posts,
        "images":images,
        "avg_rating":avg_rating
    }
    return render(request, 'company/photos.html', context)

def reviews(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    reviews = Reviews.objects.filter(company=id).order_by('-created_at')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    avg_rating = Reviews.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']
    context = {
        "reviews":page_obj,
        "company":company,
        "posts":posts,
        "avg_rating":avg_rating
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
        # register company as advitiser
        advertiser = Advertiser(company_name=companyName, website=websiteUrl, created_by=request.user)
        advertiser.save()
      
        messages.success(request, 'Company profile created successfully')
        # redirect to the company profile page
        return redirect('companyProfile', id=companyProfile.id)
        
    
    return render(request, 'company/listCompany.html')

def addReview(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    avg_rating = Reviews.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']
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
        "posts":posts,
        "avg_rating":avg_rating,
    }
    return render(request, 'company/addReview.html', context)

def likeAndDislikeCompany(request, company_id):
    company =  CompanyProfile.objects.get(id=company_id)
    user = request.user
    if Likes.objects.filter(company=company, user=user).exists():
        Likes.objects.filter(company=company, user=user).delete()
        messages.warning(request, 'You have disliked this company')
        return redirect('companyProfile', id=company_id)
    else:
        like = Likes.objects.create(company=company, user=user)
        like.save()
        messages.success(request, 'You have liked this company')
        return redirect('companyProfile', id=company_id)
def followAndUnfollowCompany(request, company_id):
    company =  CompanyProfile.objects.get(id=company_id)
    user = request.user
    if Follows.objects.filter(company=company, user=user).exists():
        Follows.objects.filter(company=company, user=user).delete()
        messages.warning(request, 'You have unfollowed this company')
        return redirect('companyProfile', id=company_id)
    else:
        follow = Follows.objects.create(company=company, user=user)
        follow.save()
        messages.success(request, 'You have followed this company')
        return redirect('companyProfile', id=company_id)

def addImages(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    avg_rating = Reviews.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']
    if request.method == 'POST':
        company = company
        user = request.user        
        image = request.FILES.get('image')
        companyPhoto = CompanyImages(company=company, image=image)
        companyPhoto.save()
        messages.success(request, 'Image added successfully')
        return redirect('companyPhotos', id=id)
    context = {
        "company":company,
        "posts":posts,
        "avg_rating":avg_rating,
    }
    return render(request, 'company/addImages.html', context)

class CompanyProfileUpdate(UpdateView):
    model = CompanyProfile
    fields = [
        "companyName",
        "description",
        "profilePicture",
        "bannerPicture",
        "category",
        "phone",
        "email",
        "websiteUrl",
        "address"

    ]
    template_name = "company/updateCompanyProfile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyProfile.objects.get(id=self.object.id)
        avg_rating = Reviews.objects.filter(company=self.object).aggregate(Avg('rating'))['rating__avg']
        context['avg_rating'] = avg_rating
        return context

    def get_success_url(self):
        return reverse_lazy('companyProfile', kwargs={'id': self.object.id})
   
    
    
