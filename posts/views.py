from django.shortcuts import render, redirect
from .models import Post, PostLikes, PostComments
from companies.models import CompanyProfile
from django.contrib import messages

# view all company posts
def allPosts(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id).order_by('-created_at')
    no_of_posts = Post.objects.filter(company=id).count()
    context = {
        "company":company,
        "posts":posts,
        "no_of_posts": no_of_posts,
    }
    return render(request, 'posts/allPosts.html', context)

def add_post(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    if request.method == 'POST':
        company = company         
        body = request.POST['body']
        image = request.FILES['image']
        post = Post.objects.create(company=company, body=body, image=image)
        post.save()
        messages.success(request, 'Post added successfully')
        
        return redirect('allPosts', id=id)
    context = {
        "company":company,
    }
    return render(request, 'posts/add_post.html', context)

def likeAndDislikePost(request, post_id, company_id):
    post_id = str(post_id)
    company_id = str(company_id)
    company = CompanyProfile.objects.get(id=company_id)
    posts = Post.objects.filter(company=company_id).order_by('-created_at')
    no_of_posts = Post.objects.filter(company=company_id).count()
    user = request.user
    post = Post.objects.get(id=post_id)
    if PostLikes.objects.filter(post=post, user=user).exists():
        PostLikes.objects.filter(post=post, user=user).delete()
        return redirect('allPosts', id=company_id)
    else:
        PostLikes.objects.create(post=post, user=user)
        return redirect('allPosts', id=company_id)

   