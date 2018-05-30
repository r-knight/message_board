from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from ..games.models import *
from ..comments.models import *

def index(request):
    if 'id' in request.session:
        return redirect('/users/success')
    response = "placeholder for index page"
    return render(request, 'users/index.html')
def existing(request):
    if 'id' in request.session:
        return redirect('/users/success')
    return render(request, 'users/login.html')
    return HttpResponse(response)
def new(request):
    if 'id' in request.session:
        return redirect('/users/success')
    response = "placeholder for register new user page"
    return render(request, 'users/register.html')
def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.session, request.POST)
        if len(errors) == 0:
            if User.objects.register_new_user(request.session, request.POST):
                return redirect('/users/success')
            else:
                print("==============Unable to register user==============")
                return redirect('/users/new')
        else:
            print("Found " + str(len(errors)) + " errors!")
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/new')
    else:
        return redirect('/users/new')
def login(request):
    if request.method == 'POST':
        user = User.objects.validate_login(request.session, request.POST)
        if user:
            return redirect('/users/success')
        else:
            messages.error(request, "The email and password provided do not match any records in our database")
            return redirect('/users/existing')
    else:
        return redirect('/users/existing')
def success(request):
    if 'id' in request.session:
        if len(User.objects.filter(id=int(request.session['id']))) > 0:
            user = User.objects.get(id=int(request.session['id']))
            request.session['name'] = user.first_name + " " + user.last_name
            return redirect('/dashboard/redirect')
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect('/')
def logout(request):
    if 'id' in request.session:
        request.session.pop('id')
    return redirect('/')
def flush_all(request):
    request.session.clear()
    messages.success(request, "Session cleared!")
    return redirect('/')
def edit(request, user_id):
    if 'id' in request.session:
        if int(request.session['id']) == int(user_id):
            user = User.objects.get(id=int(user_id))
            return render(request, 'users/edit_user.html', {'user': user})
        
        response = "Placeholder for edit profile for user "+ str(user_id) + ". Users can only edit their own profile. Current User: " + str(request.session['id'])
        return HttpResponse(response)
    else:
        response = "Placeholder for edit profile for user "+ str(user_id) + ". Users must be logged in to edit their profile."
        return HttpResponse(response)
def admin_edit(request, user_id):
    if 'id' in request.session:
        active_user = User.objects.get(id=request.session['id'])
        if active_user.account_level <=2:
            user = User.objects.get(id=int(user_id))
            request.session['to_edit'] = user_id
            return render(request, 'users/edit_user_admin.html', {'user': user, 'active_user': active_user })
        else:
            response = "Placeholder for admin_edit profile for user "+ str(user_id) + ". Users must be an admin to edit another user."
            return HttpResponse(response)
    else:
        response = "Placeholder for edit profile for user "+ str(user_id) + ". Users must be logged in to edit a profile."
        return HttpResponse(response)
def view_user(request, user_id):
    if 'id' in request.session:
        try:
            user = User.objects.get(id = int(request.session['id']))
            if len(User.objects.filter(id = int(user_id)))> 0: 
                viewed_user = User.objects.get(id = int(user_id))
                #games = Game.objects.all()
                #likes = Game.objects.all()
                #comments = Comment.objects.all()
                return render(request, 'users/profile.html', {'user': user, 'viewed_user': viewed_user})
            else:
                response = "Placeholder for view profile for user " + str(user_id) + ". This user does not yet exist."
                return HttpResponse(response)
        except:
            messages.error(request, "An error occurred. Please try logging in again.")
            del request.session['id']
            return redirect('/users/login')
    else:
        messages.error(request, "You must be logged in to view a user's profile!")
        return redirect('/')
def edit_profile(request):
    if request.method == 'POST':
        errors = User.objects.edit_validation(request.session, request.POST)
        if len(errors) == 0:
            print ("edit_profile path!")
            user = User.objects.process_edit(request.session)
            if user:
                return redirect('/users/success')
            else:
                messages.error(request, "You don't have permission to edit that profile")
                return redirect('/dashboard/redirect')
                
        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard/redirect')
    else:
        messages.error(request, "You don't have permission to view that page")
        return redirect('/dashboard/redirect')
def admin_edit_profile(request):
    if request.method == 'POST':
        errors = User.objects.edit_validation_admin(request.session, request.POST)
        print ("admin_edit_profile path, just after errors variable is set!")
        if len(errors) == 0:
            user = User.objects.process_edit_admin(request.session)
            print ("admin_edit_profile path!")
            if user:
                return redirect('/users/success')
            else:
                messages.error(request, "You don't have permission to edit that profile")
                return redirect('/dashboard/redirect')
                
        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard/redirect')
    else:
        messages.error(request, "You don't have permission to view that page")
        return redirect('/dashboard/redirect')
def admin_edit_password(request):
    if request.method == 'POST':
        errors = User.objects.validate_password_edit_admin(request.session, request.POST)
        print ("admin_edit_password path, just after errors variable is set!")
        if len(errors) == 0:
            user = User.objects.edit_password_admin(request.session, request.POST)
            print ("admin_edit_password path!")
            if user:
                return redirect('/users/success')
            else:
                messages.error(request, "You don't have permission to edit that profile")
                return redirect('/dashboard/redirect')
                
        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard/redirect')
    else:
        messages.error(request, "You don't have permission to view that page")
        return redirect('/dashboard/redirect')

def submit_new_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.session, request.POST)
        if len(errors) == 0:
            #response = "No errors! User could have been registered"
            #return HttpResponse(response)
            if User.objects.register_new_user(request.session, request.POST):
               return redirect('/users/success')
            else:
               print("==============Unable to register user==============")
               return redirect('/users/new')
        else:
            print("Found " + str(len(errors)) + " errors!")
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard/admin/add')
    else:
        return redirect('/dashboard/admin/add')

def admin_delete_profile(request):
   if request.method == 'POST':
        if 'id' in request.session:
            user = User.objects.get(id=int(request.session['id']))
            u = User.objects.delete_user(request.session)
            if u:
                print ("Deleted profile!")
                return redirect ('/dashboard/redirect')
            else:
                print ("Unable to delete user!")
                return redirect ('/dashboard/redirect')
        else:
            response = "You must be logged in to delete a user!"
            return redirect('/users/login')
   else:
        print ("Attempted to access admin_delete_profile with a GET method! As a precaution, redirected to cancel delete path")
        response = 'placeholder for admin_delete_profile (deletion confirmed path). <a href="/dashboard/admin_dashboard"> Back to dashboard </a>'
        return redirect('/users/admin_cancel_delete')
def admin_delete(request, user_id):
    if 'id' in request.session:
        user = User.objects.get(id=int(request.session['id']))
        if User.objects.can_delete_user(request.session, user_id):
            viewed_user = User.objects.get(id=int(user_id))
            request.session['to_delete'] = viewed_user.id
            games = Game.objects.filter(uploader__id = int(user_id))
            return render (request, 'users/delete_confirm.html', {'user': user, 'viewed_user': viewed_user, 'games': games})
        else:
            messages.error(request, "You cannot delete a user with greater permissions than yourself!")
            return redirect('/dashboard/redirect')
    return render(response)
def admin_cancel_delete(request):
    if 'id' in request.session:
        if 'to_delete' in request.session:
            del request.session['to_delete']
    return redirect('/dashboard/redirect')