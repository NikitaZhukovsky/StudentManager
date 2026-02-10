from django.db import models
from courses.models import Course


class Assignment(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=False)
    due_date = models.DateField(null=False, blank=False)

    def str(self):
        return f"{self.title}"

