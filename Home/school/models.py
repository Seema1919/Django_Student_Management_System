# models.py

from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    student_class = models.CharField(max_length=50)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.full_name and self.user:
            self.full_name = self.user.get_full_name() or self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name



class Subject(models.Model):
    name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.student.user.username})"


class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_classes = models.PositiveIntegerField(default=0)
    attended_classes = models.PositiveIntegerField(default=0)

    def percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.attended_classes / self.total_classes) * 100, 2)


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField()
    total_marks = models.FloatField(default=100)


def percentage(self):
    if self.total == 0:
        return 0
    return round((self.score / self.total) * 100, 2)
