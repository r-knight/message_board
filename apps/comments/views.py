from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from ..users.models import *
from ..games.models import *

def edit_comment(request, comment_id):
   response = 'placeholder for edit_comment for comment ' + str(comment_id)
   messages.error(request, "Edit feature is currently under maintenance. Please try again later!")
   return redirect('/games/list/')
def submit_edit(request, comment_id):
   response = 'placeholder for submit_edit for comment ' + str(comment_id)
   messages.error(request, "Edit feature is currently under maintenance. Please try again later!")
   return redirect('/games/list/')
def delete_comment(request, comment_id):
    if 'id' in request.session:
        try:
            errors = Comment.objects.validate_delete(request.session, comment_id)
            if len(errors) == 0:
                comment = Comment.objects.delete_comment(request.session, comment_id)
                if comment:
                    return redirect('/games/list/')
            else:
                for key, value in errors.items():
                    messages.error(request, value)
                    return redirect('/games/list/')
        except:
            messages.error(request, "An error occurred while processing your request. Please try deleting the message again.")
            return redirect('/games/list/')    
    else:
        messages.error(request, "You must be logged in to delete a commment!")
        return redirect('/')

def submit_comment(request, page_id):
    if request.method == 'POST':
        errors = Comment.objects.basic_validator_existing_page(request.session, request.POST)
        request.session['game_title'] = Game.objects.get(id=int(page_id)).title
        if len(errors) == 0:
            comment = Comment.objects.submit_comment(request.session)
            if comment:
                return redirect ('/games/' + str(comment.game.id))
        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/myaccount/' + str(request.session['id']))
    else:
        response = "This page ('submit_comment_new') can only be accessed with a POST method!"
        return HttpResponse(response)
    response = 'placeholder for submit_comment for page ' + str(page_id)
    return HttpResponse(response)
def submit_comment_new(request):
    if request.method == 'POST':
        errors = Comment.objects.basic_validator(request.session, request.POST)
        if len(errors) == 0:
            comment = Comment.objects.submit_comment(request.session)
            if comment:
                return redirect ('/games/' + str(comment.game.id))
        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/myaccount/' + str(request.session['id']))
          
    else:
        response = "This page ('submit_comment_new') can only be accessed with a POST method!"
        return HttpResponse(response)
def like_comment(request, comment_id):
    if 'id' in request.session:
        errors = Comment.objects.validate_like(request.session, comment_id)
        if len(errors) == 0:
            comment = Comment.objects.submit_like(request.session, comment_id)
            if comment:
                return redirect('/games/' + str(comment.game.id))
            else:
                response = "Unable to like selected comment! Please try again.<a href='/dashboard/dashboard'>Back to quotes</a>"
                return HttpResponse(response)

        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/games/list')
    else:
        response = "You must be logged in to like a comment!<a href='/users/login'>Login</a>"
        return HttpResponse(response)