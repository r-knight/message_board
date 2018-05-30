from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from ..games.models import *
from ..users.models import *
from ..comments.models import *

def route_to_dashboard(request):
    try:
        if 'id' in request.session:
            user = User.objects.get(id=int(request.session['id']))
            if int(user.account_level) < 3:
                return redirect('/dashboard/admin_dashboard')
            else:
                return redirect('/dashboard/dashboard')
        else:
            messages.error['not_logged_in'] = 'You must be logged in to view that page!'
            return redirect('/users/login')
    except:
        response = 'You must be logged in to a valid account to view that page!'
        if 'id' in request.session:
            del request.session['id']
        return redirect('/')
def dashboard(request):
    if 'id' in request.session:
        user = User.objects.get(id=int(request.session['id']))
        users = User.objects.all()
        return render(request, 'dashboard/dashboard.html', {'user': user, 'users': users})
    return redirect('/users/login')
def admin_dashboard(request):
    if 'id' in request.session:
        response = 'placeholder for dashboard admin_home.'# User ' + str(request.session['id']) + ' is an admin.'
        user = User.objects.get(id=int(request.session['id']))
        if user.account_level < 3:
            users = User.objects.all()
            return render(request, 'dashboard/admin_dashboard.html', {'user': user, 'users': users})
        else:
            response = 'You are not an admin!'
            return redirect('/dashboard/dashboard')
    return redirect('/users/login')
def home(request):
    response = 'placeholder for home.'
    return render(request, 'dashboard/home.html')
def add_user(request):
    if 'id' in request.session:
        response = 'placeholder for admin_add.'# User ' + str(request.session['id']) + ' is an admin.'
        user = User.objects.get(id=int(request.session['id']))
        if user.account_level < 3:
            return render(request, 'dashboard/admin_add.html', {'user': user})
        else:
            response = 'You are not an admin!'
            return redirect('/dashboard/dashboard')
    else:
        messages.error['not_logged_in'] = "You must be logged in to view that page!"
        return redirect('/users/login')