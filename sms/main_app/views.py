from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView

from main_app.models import Teacher, TeacherForm


class BaseView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'index'

    def get(self, request):
        return render(request, '__base__.html')


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
        remember_me = request.POST.get('remember', True)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('index')
        else:
            return HttpResponse('Błędny login lub hasło')


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
