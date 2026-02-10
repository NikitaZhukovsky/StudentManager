from django.db import models


class Students(models.Model):
    full_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)

    def str(self):
        return f"{self.full_name} ({self.email})"

