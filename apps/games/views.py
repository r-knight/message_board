from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from ..users.models import *
from ..comments.models import *

def submit_game(request):
    if request.method == 'POST':
        response = 'placeholder for submit_game'
        return HttpResponse(response) 
    else:
        response = 'this page can only be accessed with a POST method'
        return HttpResponse(response)
def view_game(request, game_id):
    if 'id' in request.session:
        if len(User.objects.filter(id=int(request.session['id']))) > 0:
            user = User.objects.get(id=int(request.session['id']))
        else:
            return redirect('/users/login')
        if len(Game.objects.filter(id=int(game_id))) > 0:
            game = Game.objects.get(id=int(game_id))
            request.session['last_viewed_game'] = game.id
            return render(request, 'games/view_game.html', {'user':user, 'game': game})
        else:
            return redirect('/users/login')
    else:
        response = 'placeholder for view_game for game ' + str(game_id)
        return HttpResponse(response)

def like_game(request, game_id):
    if 'id' in request.session:
        errors = Game.objects.validate_like(request.session, game_id)
        if len(errors) == 0:
            game = Game.objects.submit_like(request.session, game_id)
            if game:
                return redirect('/games/' + str(game_id))
            else:
                response = "Unable to like selected quote! Please try again.<a href='/quotes'>Back to quotes</a>"
                return HttpResponse(response)

        else:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/games/' + str(game_id))
    else:
        response = "You must be logged in to like a quote!<a href='/users/login'>Login</a>"
        return HttpResponse(response)

def list(request):
    if 'id' in request.session:
        try:
            user = User.objects.get(id=int(request.session['id']))
            comments = Comment.objects.all()
            games = Game.objects.filter(id__in=[comment.game.id for comment in comments])
            games_no_comments = Game.objects.exclude(id__in=[comment.game.id for comment in comments])
            recent = Comment.objects.all().order_by('-id')[:3]
            return render (request, 'games/list.html', {'user': user, 'games': games, 'recent': recent, 'games_without_comments': games_no_comments})
        except:
            messages.error['not_logged_in'] = "We were not able to process your request. Please log in and try again."
            return redirect('/users/login')
    else:
        messages.error['not_logged_in'] = "You must be logged in to view that page!"
        return redirect ('/')

def catch_and_redirect(request):
    return redirect ('/users/list')
