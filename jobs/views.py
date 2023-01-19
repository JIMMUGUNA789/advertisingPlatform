from django.shortcuts import render, redirect
from .models import Jobs
from posts.models import Post
from companies.models import CompanyProfile
from django.contrib import messages




# Create your views here.
def allJobs(request, company_id):
    company_id = str(company_id)
    company = CompanyProfile.objects.get(id=company_id)
    posts = Post.objects.filter(company=company_id)

    jobs = Jobs.objects.filter(company=company_id)
    context = {
        "jobs":jobs,
        "company":company,
        "posts":posts,
    }
    return render(request, 'jobs/allJobs.html', context)

def addJob(request, id):
    id = str(id)
    company = CompanyProfile.objects.get(id=id)
    posts = Post.objects.filter(company=id)
    if request.method == 'POST':
        company = company
        title = request.POST['title']
        description = request.POST['description']
        requirements = request.POST['requirements']
        salary = request.POST.get('salary')
        jobType = request.POST['jobType']
        jobLevel = request.POST['jobLevel']
        applicationDeadline = request.POST['applicationDeadline']
        noOfVacancies = request.POST['noOfVacancies']
        
        # save job
        job = Jobs.objects.create(title=title, company=company, description=description, requirements=requirements, salary=salary, jobLevel=jobLevel, jobType=jobType, applicationDeadline=applicationDeadline, noOfVacancies=noOfVacancies)

        job.save()
        messages.success(request, 'Review added successfully')
        return redirect('allJobs', company_id=id)
    context = {
        "company":company,
        "posts":posts
    }
    return render(request, 'jobs/addJob.html', context)