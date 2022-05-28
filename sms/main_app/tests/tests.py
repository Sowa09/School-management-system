from main_app.models import Student, SchoolClass
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
def test_class_modify(client):
    """
    Function should test modification view
    :param client:
    :return: asserts
    """
    sch_class = SchoolClass.objects.create(name='3', year=2020)
    response = client.post(f'/class/edit/{sch_class.id}', {'name': '6', 'year': 2021})

    assert response.status_code == 302
    sch_class.refresh_from_db()
    assert sch_class.year == 2021
    assert sch_class.name == '6'


