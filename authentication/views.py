from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import Registration
# Create your views here.



def logoutView(request):
    logout(request)
    return redirect("/")

def registerView(request):
    logout(request)
    if request.method=='POST':
        form=Registration(request.POST)

        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect("/")
    else:
        form=Registration()      

    context={
        'form':form
    }      
    return render(request,'registration/register.html',context)