import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.forms.models import ModelForm

GENDER_CHOICES = [
    ('M', 'Mężczyzna'),
    ('K', 'Kobieta')
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


def validate_year(value):
    if value < 14 or value > 99:
        raise ValidationError(f"Proszę podać poprawny wiek")


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# MODELS

class SchoolClass(models.Model):
    name = models.CharField(max_length=8)
    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(2020), max_value_current_year]
    )

    def __str__(self):
        return f'Rok: {str(self.year)} Klasa: {self.name} '


class SchoolClassForm(ModelForm):
    class Meta:
        model = SchoolClass
        fields = '__all__'


class Subject(models.Model):
    name = models.CharField(max_length=32, verbose_name='Przedmiot')
    student = models.ManyToManyField('Student')

    def __str__(self):
        return f'{self.name}'


class Teacher(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    subject = models.ManyToManyField(Subject, verbose_name='Przedmiot')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.subject}'


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class Grades(models.Model):
    grade = models.FloatField(choices=GRADES)
    subject = models.ManyToManyField(Subject)


class Student(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    age = models.IntegerField(verbose_name='Wiek', validators=[validate_year])
    grades = models.ManyToManyField(Grades)
    school_class = models.ManyToManyField(SchoolClass, verbose_name='Rok rozpoczęcia nauki/klasa')

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
