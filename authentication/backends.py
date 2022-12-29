from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth.models import User, Group
from authentication.models import Allowed
from xmlrpc.client import ServerProxy
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.contrib import messages


class LoginBackend(BaseBackend):

    domain = 'unsl.edu.ar'
   # proxy_url = 'http://unslid.unsl.edu.ar/xmlrpc/server.php?'
    proxy_url = 'http://inter10-u.unsl.edu.ar/xmlrpc/server.php?'
    mailbox_url = "mailbox.unsl.edu.ar"

    def authenticate(self, request, username=None, password=None):
        # Validate XML-RPC
        server = ServerProxy(self.proxy_url)
        validate = server.mail.validate(username, password, self.mailbox_url)
        if validate:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.set_password(password)
                user.is_staff = True
                user.email = u'%s@%s' % (username, self.domain)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
