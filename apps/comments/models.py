from django.db import models
from apps.users.models import *
from apps.games.models import *
# Create your models here.

class CommentManager(models.Manager):
    def basic_validator(self, ReqSession, ReqPost):
        errors = {}
        if ReqPost['new_comment']:
            ReqSession['comment_text'] = ReqPost['new_comment'].strip()
            if len(ReqSession['comment_text']) < 11:
                errors['comment_too_short'] = "Comment must be 11 or more characters!"
            elif len(ReqSession['comment_text']) > 1000:
                errors['comment_too_long'] = "Comment must be 1000 or fewer characters!"
        else:
            errors['comment_blank'] = "Comment must not be blank!"
        if ReqPost['game_title']:
            ReqSession['game_title'] = ReqPost['game_title'].strip()
            if len(ReqSession['game_title']) < 2:
                errors['game_title_too_short'] = "Game title must be 2 or more characters!"
        else:
            errors['game_title_blank'] = "Game title must not be blank!"
        
        return errors
    def basic_validator_existing_page(self, ReqSession, ReqPost):
        errors = {}
        if ReqPost['new_comment']:
            ReqSession['comment_text'] = ReqPost['new_comment'].strip()
            if len(ReqSession['comment_text']) < 11:
                errors['comment_too_short'] = "Comment must be 11 or more characters!"
            elif len(ReqSession['comment_text']) > 1000:
                errors['comment_too_long'] = "Comment must be 1000 or fewer characters!"
        else:
            errors['comment_blank'] = "Comment must not be blank!"
        return errors
    def submit_comment(self, ReqSession):
        if 'id' in ReqSession:
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                return False

            if 'game_title' in ReqSession:
                if len(Game.objects.filter(title=ReqSession['game_title'])) > 0:
                    game = Game.objects.get(title=ReqSession['game_title'])
                else:
                    game = Game(title=ReqSession['game_title'], uploader = user)
                    game.save()
            else:
                return False
        
            if 'comment_text' in ReqSession:
                comment = Comment(text=ReqSession['comment_text'], uploader=user, game=game)
                comment.save()
                
                del ReqSession['comment_text']
                del ReqSession['game_title']
                return comment
        return False
    def delete_selected(self, ReqSession, comment_id):
        if 'id' in ReqSession:
            if len(Comment.objects.filter(id=int(comment_id))) > 0:
                comment = Comment.objects.get(id=int(comment_id))
            else:
                return False
            if int(ReqSession['id']) == int(comment.uploader.id):
                comment.delete()
                return comment
        return False
    def validate_like(self, ReqSession, comment_id):
        errors = {}
        if 'id' in ReqSession:
            if len(Comment.objects.filter(id=int(comment_id))) > 0:
                comment = Comment.objects.get(id=int(comment_id))
            else:
                errors['comment_does_not_exist'] = "That comment does not exist!"
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                errors['user_does_not_exist'] = "That user does not exist!"
            
            if len(errors) == 0:
                if user in comment.liked_users.all():
                    errors['user_already_liked_comment'] = "You have already liked that comment!"
            return errors
        else:
            errors['not_logged_in_like'] = "You must be logged in to like a comment!"
            return errors
    def submit_like(self, ReqSession, comment_id):
        if 'id' in ReqSession:
            if len(Comment.objects.filter(id=int(comment_id))) > 0:
                comment = Comment.objects.get(id=int(comment_id))
            else:
                return False
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                return False
            if user in comment.liked_users.all():
                return False #already checked in validate_like, but used to try to prevent duplicate likes
            else:
                comment.liked_users.add(user)
                comment.save()
                return comment
        return False        
    def validate_delete(self, ReqSession, comment_id):
        errors = {}
        if 'id' in ReqSession:
            if len(Comment.objects.filter(id=int(comment_id))) > 0:
                comment = Comment.objects.get(id=int(comment_id))
            else:
                errors['comment_does_not_exist'] = "That comment does not exist!"
            
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                errors['user_does_not_exist'] = "That user does not exist!"
            
            if comment.uploader.id != user.id:
                errors['comment_not_own'] = "You can only delete your own comments!"
            return errors
        else:
            errors['not_logged_in_delete'] = "You must be logged in to like a comment!"
            return errors
    def delete_comment(self, ReqSession, comment_id):
        if 'id' in ReqSession:
            if len(Comment.objects.filter(id=int(comment_id))) > 0:
                comment = Comment.objects.get(id=int(comment_id))
            else:
                return False
            if len(User.objects.filter(id=int(ReqSession['id']))) > 0:
                user = User.objects.get(id=int(ReqSession['id']))
            else:
                return False
            if comment.uploader.id != user.id:
                return False #already checked in validate_delete, but used to try to prevent duplicate delete requests
            else:
                comment.delete()
                return True
        return False
         
class Comment(models.Model):
    text = models.TextField(default="")
    uploader = models.ForeignKey('users.User')
    game = models.ForeignKey('games.Game')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()
    liked_users = models.ManyToManyField(User, related_name="liked_comments")