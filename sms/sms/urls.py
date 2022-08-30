"""sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.templatetags.static import static


from main_app.views import LoginView, LogoutView, BaseView, TeacherListView, TeacherFormView, StudentListView, \
    StudentFormView, StudentDetailsView, SchoolClassFormView, SchoolClassListView, SchoolClassModify, \
    StudentClassDetailsView, SubjectFormView, create_user, change_password, DeleteStudentView, DeleteTeacherView, \
    AddTopicToSubject, GradesFormView, StudentTopicGradeSubjectView



urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=static('favicon.ico'))),
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', BaseView.as_view(), name='index'),
    path('new_user/', create_user, name='new-user'),
    path('change_password/', change_password, name='change-password'),
    path('teacher/list', TeacherListView.as_view(), name='teacher-list'),
    path('teacher/add', TeacherFormView.as_view(), name='teacher-add'),
    path('teacher/delete/<int:pk>', DeleteTeacherView.as_view(template_name='teacher_confirm_delete.html'),
         name='teacher-delete'),
    path('student/list', StudentListView.as_view(), name='student-list'),
    path('student/add', StudentFormView.as_view(), name='student-add'),
    path('student/delete/<int:pk>', DeleteStudentView.as_view(template_name='student_confirm_delete.html'),
         name='student-delete'),
    path('student/<int:student_id>', StudentDetailsView.as_view(), name='student-details'),
    path('class/add', SchoolClassFormView.as_view(), name='class-add'),
    path('class/list', SchoolClassListView.as_view(), name='class-list'),
    path('class/edit/<int:pk>', SchoolClassModify.as_view(template_name='school_class_update_form.html'), name='class-modify'),
    path('class/details/<int:class_id>', StudentClassDetailsView.as_view(), name='class-details'),
    path('subject/add', SubjectFormView.as_view(), name='subject-add'),
    path('topcic/add', AddTopicToSubject.as_view(), name='topic-add'),
    path('grades/add', GradesFormView.as_view(), name='grades-add'),
    path('grades/subject/list', StudentTopicGradeSubjectView.as_view(), name='grades-list'),
]
