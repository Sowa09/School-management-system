from django.db import models
from django.forms.models import ModelForm

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


# class Subject(models.Model):
#     name = models.CharField(choices=SCHOOL_SUBJECT, max_length=32)
#
#     def __str__(self):
#         return f'{self.name}'


class Teacher(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    subject_info = models.CharField(choices=SCHOOL_SUBJECT, max_length=16, verbose_name='Przedmiot')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class Student(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    age = models.IntegerField(verbose_name='Wiek')

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
