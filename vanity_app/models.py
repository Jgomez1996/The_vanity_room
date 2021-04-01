from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if len(postData['phone_number']) < 10:
            errors['phone_number'] = "Enter a valid phone numnber"
        if len(postData['email']) < 5:
            errors['email'] = "Email should be at least 5 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Your passwords don't match !"
        if not EMAIL_REGEX.match(postData['email']):
            errors['regex'] = "Email is not in the correct format"
        return errors

class User (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User: {self.first_name} ({self.id})>"

class Service (models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    duration = models.IntegerField(null=True)
    description = models.TextField()
    images = models.ImageField(null=True)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Service: {self.name} ({self.id})>"

class Appointment(models.Model):
    date = models.DateTimeField()
    booked_user = models.ForeignKey(
        User, related_name='appointments', on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, related_name='appointments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Appointment: {self.booked_user.first_name} ({self.id})>"


class Class (models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    deposit = models.IntegerField()
    description = models.TextField()
    images = models.ImageField(null=True)
    date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Class: {self.name} ({self.id})>"
