from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from log_in.models import *
from datetime import datetime

# Create your models here.


class TripManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors["destination"] = "Your destination needs some sauce"
        if len(postData['desc']) < 1:
            errors["desc"] = "Your description needs some sauce"
        if not postData['trip_start']:
            errors["trip_start"] = "Please insert a start date!"
        if not postData['trip_end']:
            errors['trip_end'] = "Please insert an end date!"
        if postData['trip_end'] and postData['trip_start']:
            if postData['trip_end'] < postData['trip_start']:
                errors["invaliddate1"] = "How do you expect to start your trip after it ended???"
            if datetime.now() > datetime.strptime(postData['trip_start'], '%Y-%m-%d'):
                errors["invaliddate2"] = "You cannot start your trip in the past nor today"
        print(errors)
        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.TextField()
    user_planned = models.ForeignKey(
        Users, related_name="planned_trips", on_delete=models.CASCADE)
    users_joined = models.ManyToManyField(
        Users, related_name="joined_trips")
    trip_start = models.DateTimeField()
    trip_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
