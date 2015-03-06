# --*-- coding:utf-8 --*--
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms

def home(request):
    html='我是主页'
    return HttpResponse(html)

class UserForm(forms.Form):
    ip=forms.CharField()
    username=forms.CharField()
    password=forms.CharField()
def register(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            return HttpResponse('OK')
    else:
        form=UserForm()
    return render_to_response('formtest.html',{'form':form})
