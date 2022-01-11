from IndexHome.models import Profile
from cryptography.fernet import Fernet
import math as m
import random as r
from IndexHome.task import SendOTP


class profile_manager():

    def search_user_with_account_mail(self, mail):
        try:
            query = Profile.objects.get(user_email=mail)
            return query
        except:
            return None

    def search_user_with_id(self, id):
        try:
            query = Profile.objects.get(account_id=id)
            return query
        except:
            return None

    def is_user_verify(self, mail):
        try:
            query = self.search_user_with_account_mail(mail)
            if query.is_verfied:
                return True
            else:
                return False
        except:
            return None

    def update_verify(self, id):
        try:
            query = self.search_user_with_id(id)
            query.is_verfied = True
            query.save()
        except:
            raise Exception("Failed (update_verify)")

    def generate_otp(self):
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        OTP = ""
        varlen = len(string)
        for i in range(6):
            OTP += string[m.floor(r.random() * varlen)]
        return OTP

    def generate_only_otp(self, id):
        try:
            query = self.search_user_with_id(id)
            query.otp = self.generate_otp()
            query.save()
            SendOTP.delay(query.user_email,query.otp)
        except:
            raise Exception("Failed (generate_only_otp)")

    def add_otp(self, id):
        try:
            key = Fernet.generate_key()
            query = self.search_user_with_id(id)
            query.key = key.decode("utf-8")
            query.otp = self.generate_otp()
            query.save()
            SendOTP.delay(query.user_email,query.otp)
        except:
            raise Exception("Failed (add_otp)")

    def verify_otp(self, id, user_input):
        try:
            query = self.search_user_with_id(id)
            if query.otp == user_input:
                return True
            else:
                return False
        except:
            raise Exception("Failed (verify_otp)")

    def add_fail_request(self, id):
        try:
            query = self.search_user_with_id(id)
            query.fail_attepmt += 1
            query.save()
            return query.fail_attepmt
        except:
            raise Exception("Failed (add_fail_request)")

    def get_fail(self, id):
        try:
            query = self.search_user_with_id(id)
            return query.fail_attepmt
        except:
            raise Exception("Failed (get_fail)")

    def reset_fail(self, id):
        try:
            query = self.search_user_with_id(id)
            query.fail_attepmt = 0
            query.save()
        except:
            raise Exception("Failed (reset_fail)")

    def reset_resend(self, id):
        try:
            query = self.search_user_with_id(id)
            query.resend_request = 0
            self.resend_code_request = 0
            query.save()
        except:
            raise Exception("Failed (reset_resend)")

    def resend_request(self, id):
        try:
            query = self.search_user_with_id(id)
            query.resend_request += 1
            query.save()
        except:
            raise Exception("Failed! (resend_request)")

    def get_otp(self, mail):
        try:
            query = self.search_user_with_account_mail(mail)
            return query.otp
        except:
            return None

    def delete_field(self, id):
        try:
            query = Profile.objects.filter(account_id=id)
            query.fail_attepmt = 0
            query.resend_request = 0
            query.otp = "" 
            query.save()
        except:
            raise Exception("Failed (delete_field)")

    def createProfile(self, user_obj, id, mail):
        try:
            profile_obj = Profile.objects.create(user=user_obj, account_id=id, user_email=mail)
            profile_obj.save()
        except:
            raise Exception("Failed (createProfile)")
    
    def check_account_id(self,id):
        try:
            return Profile.objects.filter(account_id=id).exists()
        except:
            raise Exception("Failed (check_account_id)")
    
    def check_account_id(self,id):
        try:
            return Profile.objects.filter(account_id=id).exists()
        except:
            raise Exception("Failed (check_account_id)")

    def get_key(self,id):
        query = self.search_user_with_id(id)
        return query.key.encode('utf-8')

    def get_encrypted_string(self,mail,key):
        return self.encrypt(mail.encode('utf-8'),key)
        
    def get_decrypted_string(self,mail_hash,id):
        return self.decrypt(mail_hash,self.get_key(id))

    def encrypt(self,message: bytes, key: bytes):
        return Fernet(key).encrypt(message)
    
    def decrypt(self,token: bytes, key: bytes):
        return Fernet(key).decrypt(token)