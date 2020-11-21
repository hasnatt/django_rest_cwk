from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
import uuid


class Professor(models.Model):
    name = models.CharField( max_length=50)
    code = models.CharField( max_length=3, unique = True)

    def __str__(self):
        return '%s' % self.name



class Module(models.Model):
    name = models.CharField( max_length=50)
    code = models.CharField( max_length=10, unique = True)

    def __str__(self):
        return '%s' % self.name

class ModuleState(models.Model):
    semesters = [(1,1),(2,2),]
    professors = models.ManyToManyField(Professor)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=semesters)
    year = models.PositiveSmallIntegerField(null = True)

    class Meta:
        unique_together = ['module','year','semester']

    def __str__(self):
        return '%s' % self.module + ' ' '%s' % self.year

class ProfessorRating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    ratings = [(1,1),(2,2,),(3,3),(4,4),(5,5)]
    rating = models.IntegerField(choices=ratings, null=True)
    module_state = models.ForeignKey(ModuleState, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['professor','module_state','user']


