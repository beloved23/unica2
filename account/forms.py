from django import forms

from django.contrib.auth import authenticate
import logging

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.conf import settings
#from account.models import UserProfile
import urllib, urllib2
import json
#from urllib.request import urlopen


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    username.widget= forms.TextInput(attrs={'class':'form-control', 'autofocus':'true', 'placeholder': 'Username', 'Required':'true'})
    password = forms.CharField(min_length=6, max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Password'}), label=u'Password', required=True)

    class Meta():
        model = User
        fields = ['username', 'password']

    def clean(self):
        self.user_cache = None
        cd = self.cleaned_data
        username = cd.get('username')
        password = cd.get('password')
        if username and password:

            try:
                username = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError(u"Sorry, wrong Username and Password Combination")
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u"Sorry, wrong Username and Password Combination")
            elif self.user_cache is not None and self.user_cache.is_active is False:
                raise forms.ValidationError(u'Sorry, Your Account is not Activated yet.')
             
            # try:
            
            #     params = {
            #         'username': username,
            #         'password': password
            #     }
            #     #url = settings.LDAP + urllib.parse.urlencode(params)
            #     url = settings.LDAP + urllib.urlencode(params)
            #     response = urllib2.urlopen(url).read().decode('utf8')
            #     obj = json.loads(response)
            #     if obj['IsSuccess']:
            #         email = obj['ObjectList'][0]['Email']
            #         name = obj['ObjectList'][0]['FullName'].split(' ')
            #         first_name = name[0]
            #         last_name = name[1]
            #         department = obj['ObjectList'][0]['Department']
            #         try:
            #             username = User.objects.get(username=username)
            #             username.set_password(password)
            #             username.save()
            #         except User.DoesNotExist:
            #             user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            #             user.is_staff = False
            #             user.is_superuser = False
            #             user.set_password(password)
            #             user.save()
            #             #UserProfile.objects.create(user=user)
            #         #import pdb
            #         #pdb.set_trace()
            #         self.user_cache = authenticate(username=username, password=password)
            #         if self.user_cache is None:
            #             raise forms.ValidationError(u"Sorry, wrong Username and Password Combination")
            #         elif self.user_cache is not None and self.user_cache.is_active is False:
            #             raise forms.ValidationError(u'Sorry, Your Account is not Activated yet.')
            #     else:
            #         raise forms.ValidationError(u"Sorry, wrong Username and Password Combination")
            # except Exception as ex:
            #     print (str(ex))
            #     raise forms.ValidationError(u"Sorry, wrong Username and Password Combination")
        return cd

    def get_user(self):
        return self.user_cache
