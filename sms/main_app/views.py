from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.list import ListView


from .models import Teacher, TeacherForm, Student, StudentForm, PresenceListForm


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, '__login__.html')

    def post(self, request):
        username = request.POST['uname']
        password = request.POST['psw']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Błędny login lub hasło')


class BaseView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        return render(request, '__base__.html')


# TEACHER VIEWS

class TeacherListView(LoginRequiredMixin, ListView):
    login_url = '/'
    redirect_field_name = 'index'

    model = Teacher
    template_name = 'teacher_list.html'
    context_object_name = 'teacher_list'
    queryset = Teacher.objects.all()


class TeacherFormView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        form = TeacherForm()
        return render(request, 'teacher_form.html', {'form': form})

    def post(self, request):
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher-list')
        return render(request, 'teacher_form.html', {'form': form})


# STUDENT VIEWS

class StudentListView(LoginRequiredMixin, ListView):
    login_url = '/'
    redirect_field_name = 'index'

    model = Teacher
    template_name = 'student_list.html'
    context_object_name = 'student_list'
    queryset = Student.objects.all()


class StudentFormView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        form = StudentForm()
        return render(request, 'student_form.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student-list')
        return render(request, 'student_form.html', {'form': form})


class StudentDetailsView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request, student_id):
        student_details = get_object_or_404(Student, pk=student_id)
        context = {
            'student': student_details
        }
        return render(request, 'student_details.html', context)

