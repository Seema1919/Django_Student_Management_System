from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm, StudentForm, SubjectForm
from .models import Profile, Student, Subject

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, user_type=form.cleaned_data['user_type'])
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'school/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'school/login.html', {'form': form})

@login_required
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user_type == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def teacher_dashboard(request):
    students = Student.objects.all()
    return render(request, 'school/teacher_dashboard.html', {'students': students})

@login_required
def student_dashboard(request):
    student = Student.objects.filter(name=request.user.username).first()
    subjects = Subject.objects.filter(student=student)
    total_percentage = student.total_percentage() if student else 0
    return render(request, 'school/student_dashboard.html', {
        'student': student,
        'subjects': subjects,
        'total_percentage': total_percentage
    })

@login_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)
        student.added_by = request.user
        student.save()
        return redirect('teacher_dashboard')
    return render(request, 'school/add_student.html', {'form': form})

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('teacher_dashboard')

    students = Student.objects.all()
    return render(request, 'school/dashboard.html', {
        'form': form,
        'student': student,
        'students': students
    })


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard')

@login_required
def add_subject(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = SubjectForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        subject = form.save(commit=False)
        subject.student = student
        subject.save()
        return redirect('teacher_dashboard')

    students = Student.objects.all()
    return render(request, 'school/dashboard.html', {
        'form': form,
        'student': student,
        'students': students,
        'adding_subject': True
    })
