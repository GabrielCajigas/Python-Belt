from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.


class UsersManager(models.Manager):
    def register_validator(self, postData):
        outcome = [{},
                   None]
        if len(postData['name']) < 2:
            outcome[0]["name"] = "Name name needs be at least 2 characters"
        if len(postData['username']) < 2:
            outcome[0]["username"] = "Username needs be at least 2 characters"
        else:
            userlist = Users.objects.filter(username=postData['username'])
            if len(userlist) > 0:
                outcome[0]["username"] = "Username already exist , choose a different one"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(postData['email']):
            outcome[0]['email'] = "Invalid email address!"
        else:
            userlist = Users.objects.filter(email=postData['email'].upper())
            if len(userlist) > 0:
                outcome[0]["email"] = "Email already exist"
        if len(postData['password']) < 3:
            outcome[0]["password"] = "Password needs be at least 3 characters"
        if len(postData['confirm_password']) < 3:
            outcome[0]["confirm_password"] = "Confirmed pasword needs be at least 3 characters"
        elif postData['confirm_password'] != postData['password']:
            outcome[0]["confirm_password_dont_match"] = " Password confirmation does not match"
        if len(outcome[0]) < 1:
            outcome[1] = Users.objects.create(email=postData['email'].upper(), password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode(), name=postData['name'],
                                              username=postData['username']).id
        return outcome

    def login_validator(self, postData):
        outcome = [{},
                   None]
        if postData['username'] == '':
            outcome[0]["username"] = " Username cant be empty"
        else:
            outcome[1] = 1
            if len(Users.objects.filter(username=postData['username'])) == 0:
                outcome[0]["username"] = " Username does not match an User"
            else:
                user = Users.objects.get(username=postData['username'])
                if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    outcome[0]['password'] = "Incorrect Password"
                else:
                    outcome[1] = user.id

        return outcome


class Users(models.Model):
    name = models.CharField(max_length=60)
    username = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()
