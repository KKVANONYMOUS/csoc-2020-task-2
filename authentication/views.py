from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginView(request):
    # # username = password = ''
    # if request.POST:
    #     username = request.POST['username']
    #     password = request.POST['password']

    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #             return redirect('/books/')
    # return render_to_response('registration/login.html', context_instance=RequestContext(request))
    pass

def logoutView(request):
    pass

def registerView(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            login(request,user)
            
    else:
        form=UserCreationForm()      

    context={
        'form':form
    }      
    return render(request,'registration/register.html',context)