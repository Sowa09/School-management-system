from django.db import models
from django.db.models import UniqueConstraint
from django.forms.models import ModelForm
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator

GENDER_CHOICES = [
    ('M', 'Mężczyzna'),
    ('K', 'Kobieta')
]

SCHOOL_SUBJECT = [
    ('Pol', 'Język polski'),
    ('Ang', 'Język angielski'),
    ('His', 'Historia'),
    ('Wos', 'Wiedza o społeczeństwie'),
    ('Pp', 'Podstawy przedsiębiorczości'),
    ('Geo', 'Geografia'),
    ('Biol', 'Biologia'),
    ('Chem', 'Chemia'),
    ('Fiz', 'Fizyka'),
    ('Mat', 'Matematyka'),
    ('Inf', 'Informatyka'),
]

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)

SCHOOL_START_YEAR = (
    (2015, "2015"),
    (2016, "2016"),
    (2017, "2017"),
    (2018, "2018"),
    (2019, "2019"),
    (2020, "2020"),
    (2021, "2021"),
    (2022, "2022"),
    (2023, "2023"),
    (2024, "2024"),
    (2025, "2025"),
    (2026, "2026"),
    (2027, "2027"),
    (2028, "2028"),
    (2029, "2029"),
    (2030, "2030"),
    (2031, "2031"),
    (2032, "2032"),
    (2033, "2033"),
    (2034, "2034"),
    (2035, "2035"),
    (2036, "2036"),

)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# MODELS

class Subject(models.Model):
    name = models.CharField(choices=SCHOOL_SUBJECT, max_length=32, verbose_name='Przedmiot')

    def __str__(self):
        return f'{self.name}'


class Teacher(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class Grades(models.Model):
    grade = models.FloatField(choices=GRADES)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='student_grades')
    school_subject = models.ForeignKey('Subject', on_delete=models.CASCADE)


class Student(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    age = models.IntegerField(verbose_name='Wiek')
    grades = models.ManyToManyField(Subject, through='Grades')
    school_class = models.IntegerField(choices=SCHOOL_START_YEAR, default=current_year(),
                                       verbose_name='Rok rozpoczęcia nauki',
                                       validators=[MinValueValidator(2016), max_value_current_year])

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.age}'


class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['grades']


class PresenceList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.DateTimeField()
    present = models.BooleanField(null=True)


class PresenceListForm(ModelForm):
    class Meta:
        model = PresenceList
        fields = '__all__'
