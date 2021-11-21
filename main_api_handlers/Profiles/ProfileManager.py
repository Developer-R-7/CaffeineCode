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
            raise Exception("User Not Found with that id")

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
            raise Exception("'update_verify' failed!")

    def generate_otp(self):
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        OTP = ""
        varlen = len(string)
        for i in range(6):
            OTP += string[m.floor(r.random() * varlen)]
        return OTP

    def generate_only_otp(self,id):
        try:
            query = self.search_user_with_id(id)
            query.otp = self.generate_otp()
            query.save()
        except:
            raise Exception("generate_only_otp Failed!")

    def add_otp(self, id):
        try:
            key = Fernet.generate_key()
            query = self.search_user_with_id(id)
            query.key = key.decode("utf-8")
            query.otp = self.generate_otp()
            query.save()
        except:
            raise Exception("OTP add failed!")

    def verify_otp(self,id,user_input):
        try:
            query = self.search_user_with_id(id)
            if query.otp == user_input:
                return True
            else:
                return False
        except:
            raise Exception("'verify' failed")

    def add_fail_request(self,id):
        try:
            query = self.search_user_with_id(id)
            query.fail_attepmt += 1
            query.save()
            return query.fail_attepmt
        except:
            raise Exception("Failed! 'fail otp request'")
    
    def get_fail(self,id):
        try:
            query = self.search_user_with_id(id)
            return query.fail_attepmt
        except:
            raise("'get_fail' failed!")
    
    def reset_fail(self,id):
        #try:
        query = self.search_user_with_id(id)
        query.fail_attepmt = 0
        query.save()
        #except:
            #raise Exception("'reset_fail' failed!!")
    
    def reset_resend(self,id):
        try:
            query = self.search_user_with_id(id)
            query.resend_request = 0
            self.resend_code_request = 0
            query.save()
        except:
            raise Exception("'reset_resend' failed!")


    def resend_request(self,id):
        try:
            query = self.search_user_with_id(id)
            query.resend_request +=1
            self.resend_code_request +=1
            query.save()
        except:
            raise Exception("Failed! 'resend_request'")


    def get_otp(self,mail):
        try:
            query = self.search_user_with_account_mail(mail)
            return query.otp
        except:
            return None
    
    def delete_field(self,id):
        try:
            query = Profile.objects.filter(account_id=id).update(otp=None,fail_attepmt=None)
            query.save()
        except:
            raise Exception("'delete_field' failed!")

    def createProfile(self,user_obj,id,mail):
        try:
            profile_obj = Profile.objects.create(user = user_obj,account_id=id,user_email = mail)
            profile_obj.save()
        except:
            raise Exception("Create profile failed")
    
    

