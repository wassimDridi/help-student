from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def indexx(request):
    return render(request, 'messenger.html')