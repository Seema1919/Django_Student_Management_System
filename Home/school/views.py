
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Student, Subject, Attendance, Marks
from django.contrib.auth.decorators import login_required


def home_redirect_view(request):
    return redirect('register')


from .models import Student


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        student_class = request.POST['student_class']

        if User.objects.filter(username=username).exists():
            return render(request, 'school/register.html', {'error': 'Username already taken.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        Student.objects.create(user=user, student_class=student_class)

        return redirect('login')

    return render(request, 'school/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'school/login.html')

    return render(request, 'school/login.html')






@login_required
def dashboard_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('register')

    subjects = Subject.objects.filter(student=student)
    attendance_records = Attendance.objects.filter(student=student)
    marks_records = Marks.objects.filter(student=student)

    # Calculate total attendance and marks percentage
    total_attendance_percentage = 0
    total_marks_percentage = 0
    subject_count = subjects.count()

    subject_data = []

    for subject in subjects:
        attendance = attendance_records.filter(subject=subject).first()
        marks = marks_records.filter(subject=subject).first()

        attendance_percentage = attendance.percentage() if attendance else 0
        marks_percentage = marks.percentage() if marks else 0

        subject_data.append({
            'name': subject.name,
            'attendance_percentage': attendance_percentage,
            'marks_percentage': marks_percentage
        })

        total_attendance_percentage += attendance_percentage
        total_marks_percentage += marks_percentage

    overall_attendance = round(total_attendance_percentage / subject_count, 2) if subject_count else 0
    overall_marks = round(total_marks_percentage / subject_count, 2) if subject_count else 0

    return render(request, 'school/dashboard.html', {
        'student': student,
        'subject_data': subject_data,
        'overall_attendance': overall_attendance,
        'overall_marks': overall_marks,
        'student_class': student.student_class
    })
