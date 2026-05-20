from urllib import request

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import CustomUser
# Create your views here.
from .forms import UserCreationForm, UserLoginForm
from .task import send_welcome_email

# tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    pass

account_activation_token = TokenGenerator()


def register(request):
    form=UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # user cannot login yet
            user.is_active = False
            user.save()

            # encode user id
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # generate token
            token = account_activation_token.make_token(user)

            # activation link
            domain = get_current_site(request).domain
            activate_link = (
                f"http://{domain}"
                f"{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"
            )

            # send mail with celery
            send_welcome_email.delay(
                user.email,
                user.username,
                activate_link,
            )

            return HttpResponse(
                "User created successfully. Please check your email to activate your account."
            )

    return render(request,'users/register.html',{'form':form})

def Userlogin(request):
    form=UserLoginForm()
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form .is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return HttpResponse("Logged in succeesfully")
            else:
                return HttpResponse("Invalid credentials")
    return render(request,'users/login.html',{'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Your account has been activated successfully.")
    else:
        return HttpResponse("The activation link is invalid or has expired.")


def logout_user(request):
    logout(request)
    return HttpResponse("Logged out successfully")


