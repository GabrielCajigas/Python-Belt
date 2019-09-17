from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages


def home(request):
    if request.session.has_key('userid'):
        context = {
            'user': Users.objects.get(id=request.session['userid']),
            '3book': Books.objects.all().order_by('-id')[:3],
        }
        return render(request, "home.html", context)
    else:
        return redirect("/")


def logout(request):
    try:
        del request.session['userid']
    except:
        pass
    return redirect("/")


def add(request):
    if request.method == "POST":
        if request.session.has_key('userid'):
            book = Books.objects.create(title=request.POST['title'], author=request.POST['author'],
                                        review=request.POST['review'], rating=request.POST['rating'], user=request.session['userid'])
            return redirect('/books', {'book': book.id})
        else:
            return redirect("/")
    else:
        context = {
            'user': Users.objects.get(id=request.session['userid']),

        }
        return render(request, "add.html", context)
