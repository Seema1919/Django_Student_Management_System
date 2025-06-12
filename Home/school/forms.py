from django import forms
from django.contrib.auth.models import User
from .models import Student

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
