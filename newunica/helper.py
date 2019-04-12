from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from account.models import *
#from .utils import send_email_confirmation


def is_verified_required(function=None,
                            login_url=None,
                            redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @login_required(redirect_field_name=redirect_field_name,
                        login_url=login_url)
        def _wrapped_view(request, *args, **kwargs):
            profile = UserProfile.objects.get(user=request.user)
            user_obj = User.objects.get(email=profile.user.email)
            if profile.is_verified==False:
                return redirect('account:update_profile')
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator