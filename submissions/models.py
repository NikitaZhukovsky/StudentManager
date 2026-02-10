from django.db import models
from students.models import Student
from assignments.models import Assignment


class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=False, blank=False)
    file_path = models.CharField(max_length=500, null=False, blank=False)
    submitted_at = models.DateField(null=False, blank=False)

    def str(self):
        return f"{self.student.full_name} - {self.assignment.title}"