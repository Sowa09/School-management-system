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


class Student(models.Model):
    first_name = models.CharField(max_length=32, verbose_name='Imię')
    last_name = models.CharField(max_length=32, verbose_name='Nazwisko')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=16, verbose_name='Płeć')
    age = models.IntegerField(verbose_name='Wiek')
    teacher = models.ManyToManyField(Teacher)

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


class Subject(models.Model):
    name = models.CharField(choices=SCHOOL_SUBJECT, max_length=32, verbose_name='Przedmiot')
    student = models.ManyToManyField(Student)
    teacher = models.ManyToManyField(Teacher)

    def __str__(self):
        return f'{self.name}'


class StudentGrades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADES)
