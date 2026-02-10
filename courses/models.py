from django.db import models
from students.models import Student


class Course(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=50, unique=True, null=False, blank=False)
    students = models.ManyToManyField(Student)

    def str(self):
        return f"{self.title}: {self.code}"

