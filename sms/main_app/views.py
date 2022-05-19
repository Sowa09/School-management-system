from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


class BaseView(View):
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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Błędny login lub hasło')
