from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
@login_required(login_url='signin')
def index(request):
    return redirect('/account')

def signin(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            return redirect('/')
        else :
            messages.info(request, 'Credentials  Invalide ')
            return redirect('signin')
    else :
        return render(request, 'signin.html')

def signup(request):

    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 :
            if User.objects.filter(email=email).exists() :
                messages.info(request, 'Email taken ')
                return redirect('signup')
            elif User.objects.filter(username=username).exists() :
                messages.info(request, 'Username taken ')
                return redirect('signup')
            else :
                user = User.objects.create_user(username=username , email=email , password=password)
                user.save()
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model ,id_user=user_model.id)
                new_profile.save()
                return redirect('../account/settings')
        else :
            messages.info(request, 'Password Not Matching ')
            return redirect('signup')

    else :
        return render(request, 'signup.html')