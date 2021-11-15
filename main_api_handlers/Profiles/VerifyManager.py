from IndexHome.models import Profile


class profile_manager():

    def __init__(self, mail):
        self.fail_otp_request = 0
        self.max_otp_resend = 0
        self.mail = mail

    def search_user_with_account_mail(self):
        try:
            query = Profile.objects.get(user_email=self.mail)
            return query
        except:
            return None

    def search_user_with_id(self, id):
        try:
            query = Profile.objects.get(account_id=id)
            return query
        except:
            return None

    def is_user_verify(self):
        try:
            query = self.search_user_with_account_mail(self.mail)
            if query.is_verfied:
                return True
            else:
                return False
        except:
            return None

    def update_verify(self):
        try:
            query = self.search_user_with_account_mail(self.mail)
            query.is_verfied = True
            query.save()
        except:
            return None

    def update_fail_otp(self):
        pass
