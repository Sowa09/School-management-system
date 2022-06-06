from unittest import TestCase

from django.contrib.auth import get_user_model, authenticate
from django.test import Client
from django.urls import reverse
from main_app.models import Student, SchoolClass, Teacher
import pytest
from django.contrib.auth.models import User


def create_user():
    """
    Function that creates django auth user for testing
    :return: user in django application
    """
    user = User.objects.create_user(username='testuser', password='12345')
    return user


@pytest.mark.django_db
def test_add_student_to_db():
    """
    Function test adding student to database
    :return: asserts
    """
    student = Student.objects.create(first_name='Adam', last_name='Korzeniak', age=23)
    second_student = Student.objects.create(first_name='Adama', last_name='Korzeniak1', age=24)

    assert len(Student.objects.all()) == 2
    assert Student.objects.get(first_name="Adam") == student
    assert Student.objects.get(last_name="Korzeniak") == student
    assert Student.objects.get(age=23) == student


@pytest.mark.django_db
def test_login_view_access(client):
    """
    Function test if client can log into app
    :param client:
    :return: asserts
    """

    create_user()
    response = client.post('/', {'uname': 'testuser', 'psw': '12345'})

    assert response.status_code == 302
    assert client.get('/index/').status_code == 200
    assert client.get('/student/list').status_code == 200


@pytest.mark.django_db
class SigninLogoutTest(TestCase):
    """
    Login, logout tests. Passing wrong password or username tests.
    """
    client = Client()

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12345')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12345')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='adam', password='12345')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test', password='123456')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_logout(self):
        user = authenticate(username='test', password='12345')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user is not user.is_authenticated)


@pytest.mark.django_db
class CreateUSerTest(TestCase):
    client = Client()

    def test_create_user(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        response = self.client.post('/', {'uname': 'testuser', 'psw': '12345'})
        self.assertEqual(response.status_code, 302)


@pytest.mark.django_db
class ClassUpdateTest(TestCase):
    def test_class_update(self):
        self.client = Client()
        sch_class = SchoolClass.objects.create(pk=1, name=3, year=2020)
        response = self.client.post(
            reverse('class-modify', kwargs={'pk': sch_class.id}),
            {'name': '6', 'year': 2022})

        self.assertEqual(response.status_code, 302)
        sch_class.refresh_from_db()
        self.assertEqual(sch_class.name, 6)
        self.assertEqual(sch_class.year, 2022)


@pytest.mark.django_db
def test_counting_teachers_and_students(client):
    Student.objects.create(first_name='Adam', last_name='Sokołowski', age=23)
    Student.objects.create(first_name='Adam1', last_name='Momo', age=24)
    Student.objects.create(first_name='Adam3', last_name='Kowalski', age=73)

    Teacher.objects.create(first_name='Agnieszka', last_name='Stępień')
    Teacher.objects.create(first_name='Mariola', last_name='Kałamaga')
    Teacher.objects.create(first_name='Magda', last_name='Kuternoga')
    Teacher.objects.create(first_name='Magda1', last_name='Kuternoga1')

    teacher_count = Teacher.objects.count()
    student_count = Student.objects.count()

    assert student_count == 3
    assert teacher_count == 4

