from django.contrib.auth.models import User
from connectors.Profiles.ProfileManager import profile_manager
from django.utils.crypto import get_random_string

class UserAPI(profile_manager):

    def __init__(self):
        self.user_connect = User.objects.all()
    
    def is_user_has_account(self,mail):
        return self.user_connect.filter(email=mail).exists()
    
    def create_account(self,username,mail,password):
        user_obj = self.user_connect.create(username=username, email=mail)
        user_obj.set_password(password)
        user_obj.save()
        id = self.generate_account_id()            
        while self.check_account_id(id) is True:
            id = self.generate_account_id()
        self.createProfile(user_obj,id,mail)
        self.add_otp(id)
        encrypted_string = self.get_encrypted_string(mail,self.get_key(id))
        return [encrypted_string,id]

    def generate_account_id(self):
        return int(get_random_string(8, allowed_chars='0123456789'))

    def check_same_username(self,username):
        return self.user_connect.filter(username=username).exists()
    
    def get_username(self,email):
        return (self.user_connect.get(email=email)).username

    def set_user_password(self,mail,new_password):
        query = self.user_connect.get(email=mail)
        query.set_password(new_password)
        query.save()