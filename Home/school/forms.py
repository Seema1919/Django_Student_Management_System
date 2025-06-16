from django import forms
from django.contrib.auth.models import User
from .models import Profile, Student, Subject

class UserRegistrationForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'student_class']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'attendance', 'percentage']
