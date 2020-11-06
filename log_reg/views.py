from django.shortcuts import render, HttpResponse, redirect
from app1.models import *
from log_reg.models import *
from django.contrib import messages


def register(request):
    errors=User.objects.registerValidator(request.POST)
    if errors:
        for key,value in errors.items():
            messages.error(request, value,'register')
        request.session['errorType']='register'
        return redirect('')
    else:
        User.objects.create(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        user=User.objects.get(username=request.POST['username'])
        return redirect(f'/user/{user.id}')

def login(request):
    errors=User.objects.loginValidator(request.POST)
    if errors:
        for key,value in errors.items():
            messages.error(request, value,'login')
        request.session['errorType']='login'
        return redirect('/')
    else:
        emailFilter=User.objects.filter(email=request.POST['email'])
        user= emailFilter[0]
        return redirect(f'/user/{user.id}')

def userPage(request, id):
    user=User.objects.filter(id=id)

    return render(request, 'log_reg/user.html')

def logout(request):
    request.session.clear()
    return redirect("/")