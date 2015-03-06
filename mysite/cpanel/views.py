from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('dashboard')
            else:
                return render_to_response('login.html',{'err_msg':'Account is disabled'})
        else:
            return render_to_response('login.html',{'err_msg':'Wrong username or password'})
    if request.user.is_authenticated():
        return HttpResponseRedirect('dashboard')
    else:
        return render_to_response('login.html')


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render_to_response('index.html',{'username':request.user})


