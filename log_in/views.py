from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':  # to make sure it only work when post
        # validate the input field / all at the same time!
        outcome = Users.objects.register_validator(request.POST)
        if len(outcome[0]) > 0:  # outcome[0] is = to errors
            for key, value in outcome[0].items():
                # get all the errors to display later
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            request.session['user_id'] = outcome[1]  # outcome at  1 = userid!
            return redirect('/travels')
    else:
        return render(request, "login.html")


def login(request):
    if request.method == 'POST':
        outcome = Users.objects.login_validator(request.POST)
        if len(outcome[0]) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in outcome[0].items():
                messages.error(request, value, extra_tags='login')
                # redirect the user back to the form to fix the errors
                return redirect('/')
        else:
            request.session['user_id'] = outcome[1]  # outcome at  1 = userid!
            return redirect('/travels')

# if we didn't find anything in the database by searching by username or if the passwords don't match,
# redirect back to a safe route
    return redirect("/")


def logoff(request):
    request.session.clear()
    return redirect('/')
