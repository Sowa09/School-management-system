import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from django.forms.models import ModelForm

GENDER_CHOICES = [
    ('M', 'Mężczyzna'),
    ('K', 'Kobieta')
]

validate_only_letters = RegexValidator(r'^[^\W\d_]*$', 'Proszę podać litery')


def validate_year(value):
    """
    Year validation for student-age needs
    :param value:
    :return:Year Validation
    """
    if value < 16 or value > 80:
        raise ValidationError("Proszę podać wiek z zakresu 16-80")


def current_year():
    """
    Function that returns current year
    :return: current year
    """
    return datetime.date.today().year


def max_value_current_year(value):
    """
    Function that validates field year of school-class model, '+1' means that user can add only one year ahead.
    :param value:
    :return:
    """
    return MaxValueValidator(current_year() + 1)(value)


def validate_grades(value):
    if value < 1 or value > 6:
        raise ValidationError('Ocena musi być z przedziału 1-6')


# MODELS

class SchoolClass(models.Model):
    name = models.CharField(max_length=8, verbose_name='Nazwa')
    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(2020), max_value_current_year], verbose_name='Rok')

    class Meta:
        unique_together = ['name', 'year']

    def __str__(self):
        return f'Rok: {str(self.year)} Klasa: {self.name} '


class SchoolClassForm(ModelForm):
    class Meta:
        model = SchoolClass
        fields = '__all__'


class Subject(models.Model):
    name = models.CharField(max_length=32, verbose_name='Przedmiot', unique=True)
    student = models.ManyToManyField('Student')

    def __str__(self):
        return f'{self.name}'


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class Teacher(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię', validators=[validate_only_letters])
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko', validators=[validate_only_letters])
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    subject = models.ManyToManyField(Subject, verbose_name='Przedmiot')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.subject}'


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class Student(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię', validators=[validate_only_letters])
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko', validators=[validate_only_letters])
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    age = models.IntegerField(verbose_name='Wiek', validators=[validate_year])
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, default=None, null=True, verbose_name='Rok rozpoczęcia nauki/klasa')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.age}'


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class PresenceList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.DateTimeField()
    present = models.BooleanField(null=True)


class PresenceListForm(ModelForm):
    class Meta:
        model = PresenceList
        fields = '__all__'


class SchoolSubjectTopics(models.Model):
    name = models.CharField(max_length=64)
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.name}'


class SchoolSubjectTopicsForm(ModelForm):
    class Meta:
        model = SchoolSubjectTopics
        fields = '__all__'


class Grades(models.Model):
    grade = models.FloatField(max_length=8, verbose_name='Ocena', validators=[validate_grades])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Przedmiot')
    topic = models.ManyToManyField(SchoolSubjectTopics, verbose_name='Temat')
    student = models.ManyToManyField(Student, verbose_name='Uczeń')


class GradesForm(ModelForm):
    class Meta:
        model = Grades
        fields = '__all__'
