from django.shortcuts import render, redirect;
from django.http import HttpResponse;
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from loginSystem import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "login/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Try other usenames.")
            return redirect('signup')
            
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered.")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username must be less than 10")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "password didn't match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "Your account has been successfully created")
        
        # Welcome email
        subject = "Welcome to Ash website - Django login"
        message = "Hello " + myuser.first_name + "!! \n " + """ 
            Welcome to Ash website \n Thank you for visiting the website \n We've also sent a confirmation email,
            please confirm your email address to activate your email account. \n\n Thank you.
        
        """
        
        fromm_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, fromm_email, to_list, fail_silently=True)
        
        return redirect('signin')
    
    return render(request, "login/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "login/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    
    return render(request, "login/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully.")

    return redirect('home')
