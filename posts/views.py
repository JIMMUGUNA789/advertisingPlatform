from django.shortcuts import render
from .models import Post
from companies.models import CompanyProfile

# view all company posts
def allPosts(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    context = {
        "company":company,
        "posts":posts,
    }
    return render(request, 'posts/allPosts.html', context)