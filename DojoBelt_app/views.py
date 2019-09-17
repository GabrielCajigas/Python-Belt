from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
from django.db.models import Q


def travels(request):
    # user = request.session['user_id']
    # print(user)
    if request.session.get('user_id') != None:
        loggeduser = Users.objects.get(id=request.session['user_id'])
        context = {
            "loggeduser": loggeduser,
            "trips": Trip.objects.filter(Q(user_planned=loggeduser) | Q(users_joined=loggeduser)).distinct(),
            "users": Users.objects.all().exclude(id=loggeduser.id),
            "alltrips": Trip.objects.all(),
        }
        print(context["trips"])
        print(Trip.objects.filter(users_joined=loggeduser))
        print(Trip.objects.filter(user_planned=loggeduser))
        return render(request, "travels.html", context)
    else:
        return redirect('/')


def add(request):
    if request.session.get('user_id') != None:
        context = {
            "loggeduser": Users.objects.get(id=request.session['user_id'])
        }
        return render(request, "add.html", context)
    else:
        return redirect("/")


def addtrip(request):
    if request.session.get('user_id') != None:
        errors = Trip.objects.basic_validator(request.POST)
        print(errors)
        if len(errors):

            for tag, error in errors.items():

                messages.error(request, error)
                return redirect("travels/add")

        else:
            destination = request.POST['destination']
            description = request.POST['desc']
            tripstart = request.POST['trip_start']
            tripend = request.POST['trip_end']
            userplanned = Users.objects.get(id=request.session['user_id'])
            Trip.objects.create(destination=destination, desc=description,
                                user_planned=userplanned, trip_start=tripstart, trip_end=tripend)
        return redirect("/travels")
    else:
        return redirect("/")


def showtrip(request, id):
    if request.session.get('user_id') != None:
        user = Users.objects.get(id=request.session['user_id'])
        tripid = id
        context = {
            "trip": Trip.objects.filter(id=tripid),
            "joinedusers": Users.objects.filter(joined_trips=tripid),
            "user": user,
        }
        return render(request, "thetrip.html", context)
    else:
        return redirect("/")


def join(request, id):
    if request.session.get('user_id') != None:
        tripid = id
        T = Trip.objects.get(id=tripid)
        T.users_joined.add(request.session['user_id'])
        T.save()
        return redirect('travels/destination/' + tripid)
    else:
        return redirect("/")
