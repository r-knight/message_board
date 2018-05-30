from django.db import models
import bcrypt
import re

DEFAULT_USER_LEVEL = 3 #1 for admin, 2 for mod, 3 for standard user
r = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
def isValidEmail(email):
    if len(email) > 7:
        if re.match(r, email) != None:
            return True
    return False

class UserManager(models.Manager):
    def basic_validator(self, ReqSession, ReqPost):
        errors = {}
        if ReqPost['first_name']:
            ReqSession['first_name'] = ReqPost['first_name'].strip()
            if len(ReqSession['first_name']) < 2:
                errors['first_name_too_short'] = "First name must be 2 or more characters!"
        else:
            errors['first_name_blank'] = "First name must not be blank!"
        if ReqPost['last_name']:
            ReqSession['last_name'] = ReqPost['last_name'].strip()
            if len(ReqSession['last_name']) < 2:
                errors['last_name_too_short'] = "Last name must be 2 or more characters!"
        else:
            errors['last_name_blank'] = "Last name must not be blank!"
        if ReqPost['email']:
            ReqSession['email'] = ReqPost['email']
            if not isValidEmail(ReqSession['email']):
                errors['email_invalid'] = "Email must be valid!"
            elif len(User.objects.filter(email=ReqSession['email'])) > 0:
                errors['email_already_registered'] = "An account with that email already exists!"
        else:
            errors['email_blank'] = "Email must not be blank!"
        if ReqPost['password']:
            if len(ReqPost['password']) < 8:
                errors['password_short'] = "Password must contain at least 8 characters!"
            elif ReqPost['password'].isalpha():
                errors['password_all_letters'] = "Password must contain at least one non-letter character!"
            elif ReqPost['password'] == ReqPost['password'].lower():
                errors['password_all_lowercase'] = "Password must contain at least one uppercase letter!"
            else:
                hash1 = bcrypt.hashpw(ReqPost['password'].encode(), bcrypt.gensalt())
                if (ReqPost['password_confirm']):
                    if not bcrypt.checkpw(ReqPost['password_confirm'].encode(), hash1):
                        errors['password_mismatch'] = "Password and password confirmation must match!"
                else:
                    errors['password_confirm_blank'] = "Password confirmation must not be blank!"
        else:
            errors['password_blank'] = "Password must not be blank!"
            if not ReqPost['password_confirm']:
                errors['password_confirm_blank'] = "Password confirmation must not be blank!"
        return errors
    def register_new_user(self, ReqSession, ReqPost):
        try:
            hash1 = bcrypt.hashpw(ReqPost['password'].encode(), bcrypt.gensalt())
            u = User(first_name = ReqSession['first_name'], last_name = ReqSession['last_name'], email=ReqSession['email'], pwhash = hash1)
            u.save()
            if 'id' not in ReqSession:
                ReqSession['id'] = u.id
            return u
        except:
            print ("Something went wrong. Please try registering again.")
            return False
    def validate_login(self, ReqSession, ReqPost):
        try:
            ReqSession['e_email'] = ReqPost['e_email'].lower()
            if len(User.objects.filter(email = ReqSession['e_email'].lower())) > 0:
                user = User.objects.get(email = ReqSession['e_email'])
                if ReqPost['e_password']:
                    if bcrypt.checkpw(ReqPost['e_password'].encode(), user.pwhash.encode()):
                        ReqSession.clear()
                        ReqSession['id'] = user.id
                        return user
                return False
            else:
                return False
        except:
            print("Something went wrong. Please try logging in again.")
            return False
    def edit_validation(self, ReqSession, ReqPost):
        errors = {}
        if 'id' in ReqSession:
            try:
                user = User.objects.get(id=int(ReqSession['id']))
                if ReqPost['first_name'] and ReqPost['last_name'] and ReqPost['email']:
                    if ReqPost['first_name'] == user.first_name and ReqPost['last_name'] == user.last_name and ReqPost['email'] == user.email:
                        errors['no_changes'] = "No changes were made!"
                        return errors
                if ReqPost['first_name']:
                    ReqSession['first_name'] = ReqPost['first_name'].strip()
                    if len(ReqSession['first_name']) < 2:
                        errors['first_name_too_short'] = "First name must be 2 or more characters!"
                else:
                    errors['first_name_blank'] = "First name must not be blank!"
                if ReqPost['last_name']:
                    ReqSession['last_name'] = ReqPost['last_name'].strip()
                    if len(ReqSession['last_name']) < 2:
                        errors['last_name_too_short'] = "Last name must be 2 or more characters!"
                else:
                    errors['last_name_blank'] = "Last name must not be blank!"
                if ReqPost['email']:
                    ReqSession['email'] = ReqPost['email']
                    if not isValidEmail(ReqSession['email']):
                        errors['email_invalid'] = "Email must be valid!"
                    elif len(User.objects.filter(email=ReqSession['email'])) > 0:
                        if ReqSession['email'] != user.email:
                            print ("This is in edit_validation, not edit_validation_admin!")
                            print (user.email)
                            print (ReqSession['email'])
                            errors['email_already_registered'] = "An account with that email already exists!"
                else:
                    errors['email_blank'] = "Email must not be blank!"
                return errors
            except:
                errors['edit_failed'] = "We were unable to process your request. Please check your data and cookies and try again."
                return errors
        else:
            errors['not_logged_in'] = "You must be logged in to edit your profile."
            return errors
    def edit_validation_admin(self, ReqSession, ReqPost):
        errors = {}
        if 'id' in ReqSession and 'to_edit' in ReqSession:
            try:
                user = User.objects.get(id=ReqSession['to_edit'])
                print ('got user in edit_validation_admin')
                if ReqPost['first_name'] and ReqPost['last_name'] and ReqPost['email'] and ReqPost['user_level']:
                    if ReqPost['first_name'] == user.first_name and ReqPost['last_name'] == user.last_name and ReqPost['email'] == user.email and ReqPost['user_level'] == user.account_level:
                        errors['no_changes'] = "No changes were made!"
                        return errors
                print ('got through first check (validating all info exists) in edit_validation_admin')
                if ReqPost['first_name']:
                    ReqSession['first_name'] = ReqPost['first_name'].strip()
                    if len(ReqSession['first_name']) < 2:
                        errors['first_name_too_short'] = "First name must be 2 or more characters!"
                else:
                    errors['first_name_blank'] = "First name must not be blank!"
                print ('got through first name in edit_validation_admin')
                if ReqPost['last_name']:
                    ReqSession['last_name'] = ReqPost['last_name'].strip()
                    if len(ReqSession['last_name']) < 2:
                        errors['last_name_too_short'] = "Last name must be 2 or more characters!"
                else:
                    errors['last_name_blank'] = "Last name must not be blank!"
                print ('got through last name in edit_validation_admin')
                if ReqPost['email']:
                    ReqSession['email'] = ReqPost['email']
                    if not isValidEmail(ReqSession['email']):
                        errors['email_invalid'] = "Email must be valid!"
                    elif len(User.objects.filter(email=ReqSession['email'])) > 0:
                        if ReqSession['email'] != user.email:
                            print (user.email)
                            print (ReqSession['email'])
                            errors['email_already_registered'] = "An account with that email already exists!"
                else:
                    errors['email_blank'] = "Email must not be blank!"
                print ('got through email in edit_validation_admin')
                if ReqPost['user_level']:
                    ReqSession['user_level'] = ReqPost['user_level']
                    try:
                        if int(ReqSession ['user_level']) < 1 or int(ReqSession['user_level']) > 3:
                            print ("checked user level > 0 and < 4")
                            ReqSession['user_level'] = DEFAULT_USER_LEVEL
                    except:
                            errors['invalid_user_level'] = "User level invalid!"
                else:
                    ReqSession['user_level'] = DEFAULT_USER_LEVEL
                print ('got through user_level in edit_validation_admin')
                return errors
            except:
                errors['edit_failed'] = "We were unable to process your request. Please check your data and cookies and try again."
                return errors
        else:
            errors['not_logged_in'] = "You must be logged in to edit your profile."
            return errors

    def process_edit(self, ReqSession):
        try:
            print("--------TRYING TO UPDATE USER-------------")
            if 'id' in ReqSession: 
                user = User.objects.get(id=int(ReqSession['id']))
                if 'first_name' in ReqSession and 'last_name' in ReqSession and 'email' in ReqSession:
                    print("==========USER EMAIL PRE PROCESS===========")
                    print(user.email)
                    user.first_name = ReqSession['first_name']
                    user.last_name = ReqSession['last_name']
                    user.email = ReqSession['email']
                    user.save()
                    print("==========USER EMAIL POST PROCESS===========")
                    print(user.email)
                    del ReqSession['first_name']
                    del ReqSession['last_name']
                    del ReqSession['email']

                    return user
            return False
        except:
            print("--------FAILED TO UPDATE USER-------------")
            return False
    def process_edit_admin(self, ReqSession):
        try:
            print("--------TRYING TO UPDATE USER-------------")
            if 'id' in ReqSession: 
                user = User.objects.get(id=int(ReqSession['to_edit']))
                if 'first_name' in ReqSession and 'last_name' in ReqSession and 'email' in ReqSession and 'user_level' in ReqSession:
                    print("==========USER LEVEL PRE PROCESS===========")
                    print(user.account_level)
                    user.first_name = ReqSession['first_name']
                    user.last_name = ReqSession['last_name']
                    user.email = ReqSession['email']
                    user.account_level = ReqSession['user_level']
                    user.save()
                    print("==========USER LEVEL POST PROCESS===========")
                    print(user.account_level)
                    del ReqSession['first_name']
                    del ReqSession['last_name']
                    del ReqSession['email']
                    del ReqSession['user_level']
                    del ReqSession['to_edit']

                    return user
            return False
        except:
            print("--------FAILED TO UPDATE USER-------------")
            return False
    def validate_password_edit(self, ReqSession, ReqPost):
        errors = {}
        if 'id' in ReqSession:
            if ReqPost['password']:
                if len(ReqPost['password']) < 8:
                    errors['password_short'] = "Password must contain at least 8 characters!"
                elif ReqPost['password'].isalpha():
                    errors['password_all_letters'] = "Password must contain at least one non-letter character!"
                elif ReqPost['password'] == ReqPost['password'].lower():
                    errors['password_all_lowercase'] = "Password must contain at least one uppercase letter!"
                else:
                    hash1 = bcrypt.hashpw(ReqPost['password'].encode(), bcrypt.gensalt())
                    if (ReqPost['password_confirm']):
                        if not bcrypt.checkpw(ReqPost['password_confirm'].encode(), hash1):
                            errors['password_mismatch'] = "Password and password confirmation must match!"
                    else:
                        errors['password_confirm_blank'] = "Password confirmation must not be blank!"
            else:
                errors['password_blank'] = "Password must not be blank!"
                if not ReqPost['password_confirm']:
                    errors['password_confirm_blank'] = "Password confirmation must not be blank!"
            return errors
        else:
            errors['not_logged_in'] = "You must be logged in to edit your password!"
            return errors
    def validate_password_edit_admin(self, ReqSession, ReqPost):
        errors = {}
        if 'id' in ReqSession:
            user = User.objects.get(id=ReqSession['id'])
            if user.account_level >= DEFAULT_USER_LEVEL:
                errors['not_admin'] = "You do not have permission to change passwords on this page!"
                return errors
            if ReqPost['password']:
                if len(ReqPost['password']) < 8:
                    errors['password_short'] = "Password must contain at least 8 characters!"
                elif ReqPost['password'].isalpha():
                    errors['password_all_letters'] = "Password must contain at least one non-letter character!"
                elif ReqPost['password'] == ReqPost['password'].lower():
                    errors['password_all_lowercase'] = "Password must contain at least one uppercase letter!"
                else:
                    hash1 = bcrypt.hashpw(ReqPost['password'].encode(), bcrypt.gensalt())
                    if (ReqPost['password_confirm']):
                        if not bcrypt.checkpw(ReqPost['password_confirm'].encode(), hash1):
                            errors['password_mismatch'] = "Password and password confirmation must match!"
                    else:
                        errors['password_confirm_blank'] = "Password confirmation must not be blank!"
            else:
                errors['password_blank'] = "Password must not be blank!"
                if not ReqPost['password_confirm']:
                    errors['password_confirm_blank'] = "Password confirmation must not be blank!"
            if 'to_edit' in ReqSession:
                if len(User.objects.filter(id=ReqSession['to_edit'])) == 0:
                    errors['user_not_found'] = "User with the specified id not found!"
            else:
                errors['no_user_id'] = "No user id for targeted user found!"
            return errors
        else:
            errors['not_logged_in'] = "You must be logged in to edit your password!"
            return errors
        return "This is placeholder"
    def edit_password(self, ReqSession, ReqPost):
        try:
            hash1 = bcrypt.hashpw(ReqPost['password'].encode(), bcrypt.gensalt())
            u = User.objects.get(id=ReqSession['id'])
            u.pwhash = hash1
            u.save()
            return True
        except:
            print ("Something went wrong. Please try changing your password again.")
            return False
        return "This is placeholder"
    def edit_password_admin(self, ReqSession, ReqPost):
        if 'id' in ReqSession and 'to_edit' in ReqSession:
            user = User.objects.get(id=ReqSession['id'])
            if user.account_level <= DEFAULT_USER_LEVEL:
                try:
                    print ("before hash")
                    hash1 = bcrypt.hashpw(ReqPost['password'].encode(), bcrypt.gensalt())
                    print ("after hash, before getting user object")
                    u = User.objects.get(id=ReqSession['to_edit'])
                    print ("after getting user object, before setting user object pw")
                    u.pwhash = hash1
                    print ("after setting user object pw, before saving")
                    u.save()
                    print ("after saving user object , before deleting to_edit from session")
                    del ReqSession['to_edit']
                    print ("after deleting to_edit from session")
                    return True
                except:
                    print ("Something went wrong. Please try changing your password again.")
                    return False
            else:
                print ("Invalid permissions!")
                return False
        else:
            print("Not logged in!")
            return False
    def can_delete_user(self, ReqSession, target_id):
        #checks to see if target can be deleted. called before confirmation page is displayed
        if 'id' in ReqSession:
            user = User.objects.get(id=ReqSession['id'])
            if user.account_level <= DEFAULT_USER_LEVEL:
                try:
                    u = User.objects.get(id=target_id)
                    if user.account_level < u.account_level:
                        return True
                    else:
                        print ("User attempted delete a user that has a lower account level (lower levels have greater permissions)")
                except:
                    print ("Could not find target user.")
                    return False
            else:
                print ("Invalid permissions!")
                return False
        else:
            print("Not logged in!")
            return False
    def delete_user(self, ReqSession):
        #similar logic to can_delete_user, but actually processes delete. Called when confirming delete request.
        if 'id' in ReqSession and 'to_delete' in ReqSession:
            user = User.objects.get(id=ReqSession['id'])
            if user.account_level <= DEFAULT_USER_LEVEL:
                try:
                    u = User.objects.get(id=ReqSession['to_delete'])
                    if user.account_level < u.account_level:
                        u.delete()
                        del ReqSession['to_delete']
                        return u
                    else:
                        print ("User attempted delete a user that has a lower account level (lower levels have greater permissions)")
                        return False
                except:
                    print ("Something went wrong. Please try the delete request again.")
                    return False
            else:
                print ("Invalid permissions!")
                return False
        else:
            print("Not logged in!")
            return False
    
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255, null=True)
    email = models.CharField(max_length = 255)
    pwhash = models.CharField(max_length = 255)
    objects = UserManager()
    account_level = models.PositiveSmallIntegerField(default = 3)