from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post, PostLikes, PostComments
from companies.models import CompanyProfile
from django.contrib import messages
from django.core.paginator import Paginator

# view all company posts
def allPosts(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id).order_by('-created_at')
    no_of_posts = Post.objects.filter(company=id).count()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "company":company,
        "posts": page_obj,
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
    postLikes = 0
    if PostLikes.objects.filter(post=post, user=user).exists():
        PostLikes.objects.filter(post=post, user=user).delete()
        postLikes = PostLikes.objects.filter(post=post).count()
        return redirect('allPosts', id=company_id)
        # return JsonResponse({'postLikes':postLikes}, content_type='application/json')
    else:
        PostLikes.objects.create(post=post, user=user)
        postLikes = PostLikes.objects.filter(post=post).count()
        return redirect('allPosts', id=company_id)
        # return JsonResponse({'postLikes':postLikes}, content_type='application/json')

def deletePost(request, post_id, company_id):
    post_id = str(post_id)
    company_id = str(company_id)    
    post = Post.objects.get(id=post_id)
    post.delete()
    messages.success(request, 'Post deleted successfully')
    return redirect('allPosts', id=company_id)

def addComment(request, post_id, company_id):
    post_id = str(post_id)
    company_id = str(company_id)
    user = request.user
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        PostComments.objects.create(post=post, user=user, comment=comment)
        messages.success(request, 'Comment added successfully')
        return redirect('allPosts', id=company_id)
    
    # redirect to all posts page
    return redirect('allPosts', id=company_id)
   