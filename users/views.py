from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

# password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from users.models import CustomUser
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        print("method is post")
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            user = form.save()
            login(request, user)
            messages.success(request, "registration successful. ")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. ")
        # print form errors
        print(form.errors)
    form = RegistrationForm()
    context ={
        'register_form':form,
    }
    return render(request, 'auth/register.html', context)

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {
        "login_form":form,
    }
    return render(request, 'auth/login.html', context)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Request"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Digiverse',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        "user":user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'jimmuguna@yahoo.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    context = {
        "password_reset_form":password_reset_form,
    }
    return render(request, 'password/password_reset.html', context)


   