from django.db import models
from apps.users.models import *
from apps.comments.models import *

DEFAULT_GAMETYPE_ID = 1
class GameManager(models.Manager):
    def basic_validator(self, ReqSession, ReqPost):
        errors = {}
        if ReqPost['game_title']:
            ReqSession['game_title'] = ReqPost['game_title'].strip()
            if len(ReqSession['game_title']) < 2:
                errors['game_title_too_short'] = "Game title must be 4 or more characters!"
        else:
            errors['game_title'] = "Author name must not be blank!"
        if 'id' in ReqSession:
            if len(User.objects.filter(id=int(ReqSession['id']))):
                user = User.objects.get(id=int(ReqSession['id']))
            ReqSession['quote_text'] = ReqPost['new_quote'].strip()
        else:
            errors['not_logged_in'] = "You must be logged in to submit a game!"
        if ReqPost['type']:
            ReqSession['type'] = ReqPost['type']
            if len(GameType.objects.filter(id=int(ReqSession['type']))):
                type = GameType.objects.get(id=int(ReqSession['type']))
            else:
                ReqSession['type'] = DEFAULT_GAMETYPE_ID
        else:
            ReqSession['type'] = DEFAULT_GAMETYPE_ID
        return errors
    def submit_game(self, ReqSession):
        if 'id' in ReqSession:
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                return False
        
            if 'game_title' in ReqSession and 'type' in ReqSession:
                game = Game(title=ReqSession['game_title'], type=GameType.objects.get(id=ReqSession['type']), uploader=user)
                game.save()
                
                del ReqSession['game_title']
                del ReqSession['game_title']
                return game
        return False
    def delete_selected(self, ReqSession, game_id):
        if 'id' in ReqSession:
            if len(Game.objects.filter(id=int(game_id))) > 0:
                game = Game.objects.get(id=int(game_id))
            else:
                return False
            if int(ReqSession['id']) == int(game.uploader.id):
                game.delete()
                return game
        return False
    def validate_like(self, ReqSession, game_id):
        errors = {}
        if 'id' in ReqSession:
            if len(Game.objects.filter(id=int(game_id))) > 0:
                game = Game.objects.get(id=int(game_id))
            else:
                errors['game_does_not_exist'] = "That game does not exist!"
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                errors['user_does_not_exist'] = "That user does not exist!"
            
            if len(errors) == 0:
                if user in game.liked_users.all():
                    errors['user_already_liked_game'] = "You have already liked that game!"
            return errors
        else:
            errors['not_logged_in_like'] = "You must be logged in to like a game!"
            return errors
    def submit_like(self, ReqSession, game_id):
        if 'id' in ReqSession:
            if len(Game.objects.filter(id=int(game_id))) > 0:
                game = Game.objects.get(id=int(game_id))
            else:
                return False
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                return False
            if user in game.liked_users.all():
                return False #already checked in validate_like, but used to try to prevent duplicate likes
            else:
                game.liked_users.add(user)
                game.save()
                print ("user liked a game!", "User:", user.id, "; Game:", game.id)
                return game
        return False

class GameType(models.Model):
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Game(models.Model):
    title = models.CharField(max_length = 255)
    uploader = models.ForeignKey('users.User')
    type = models.ForeignKey('GameType', default=DEFAULT_GAMETYPE_ID)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = GameManager()
    liked_users = models.ManyToManyField(User, related_name="liked_games")
