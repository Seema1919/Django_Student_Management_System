from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=20)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # The teacher who added

    def total_percentage(self):
        subjects = self.subject_set.all()
        if subjects.exists():
            return sum(subject.percentage for subject in subjects) / subjects.count()
        return 0

class Subject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    attendance = models.CharField(max_length=10)
    percentage = models.FloatField()
