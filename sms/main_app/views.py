from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Teacher, TeacherForm, Student, StudentForm, SchoolClassForm, SchoolClass, \
    SubjectForm, SchoolSubjectTopicsForm, GradesForm


class LogoutView(View):
    """
    Simple logout view.
    """

    def get(self, request):
        logout(request)
        return redirect('login')


class LoginView(View):
    """
    Simple class permitting user to log into account and let him see the resources of web.

    Attributes
    username : str
        username necessary to login
    password : int, str
        hidden password necessary to log into account

    """

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


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    """
    Function where superuser can create new user
    :param request:
    :return:new user from django 'User' model
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required()
def change_password(request):
    """
    Function that allows user to change his password
    :param request:
    :return: new password
    """

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało zmienione!')
            return redirect('change-password')
        else:
            messages.error(request, 'Proszę o poprawienie błędów.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
    })


class BaseView(LoginRequiredMixin, View):
    """
    Base view with counter function.
    """

    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        teacher_counter = Teacher.objects.count()
        student_counter = Student.objects.count()
        ctx = {'teacher_counter': teacher_counter,
               'student_counter': student_counter}
        return render(request, '__base__.html', ctx)


# TEACHER

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


class DeleteTeacherView(LoginRequiredMixin, DeleteView):
    login_url = '/'
    redirect_field_name = 'index'

    model = Teacher
    success_url = reverse_lazy('teacher-list')


# STUDENT

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


class DeleteStudentView(LoginRequiredMixin, DeleteView):
    login_url = '/'
    redirect_field_name = 'index'

    model = Student
    success_url = reverse_lazy('student-list')


# CLASS

class SchoolClassListView(LoginRequiredMixin, ListView):
    login_url = '/'
    redirect_field_name = 'index'

    model = SchoolClass
    template_name = 'school_class_list.html'
    context_object_name = 'class_list'
    queryset = SchoolClass.objects.all().order_by('name')


class SchoolClassFormView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        form = SchoolClassForm
        return render(request, 'school_class_form.html', {'form': form})

    def post(self, request):
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'school_class_form.html', {'form': form})
        return render(request, 'school_class_form.html', {'form': form})


class SchoolClassModify(LoginRequiredMixin, UpdateView):
    """
    Class that permit user to modify view.
    """

    login_url = '/'
    redirect_field_name = 'index'

    model = SchoolClass
    fields = '__all__'
    template_name = 'school_class_update_form.html'
    success_url = '/class/list'

    def post(self, request, *args, **kwargs):
        print('POST', request.POST, kwargs)
        return super().post(request, *args, **kwargs)


class StudentClassDetailsView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request, class_id):
        class_details = get_object_or_404(SchoolClass, pk=class_id)
        students = Student.objects.filter(school_class=class_id)
        context = {
            'class': class_details,
            'students': students,
        }
        return render(request, 'class_details.html', context)


# SUBJECT

class SubjectFormView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        form = SubjectForm
        return render(request, 'subject_form.html', {'form': form})

    def post(self, request):
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'subject_form.html', {'form': form})
        return render(request, 'subject_form.html', {'form': form})


class AddTopicToSubject(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        form = SchoolSubjectTopicsForm
        return render(request, 'topic_form.html', {'form': form})

    def post(self, request):
        form = SchoolSubjectTopicsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'topic_form.html', {'form': form})


# GRADES

class GradesFormView(LoginRequiredMixin, FormView):
    login_url = '/'
    redirect_field_name = 'index'

    template_name = 'add_grade.html'
    form_class = GradesForm
    success_url = '/grades/add'
