from django.db import models

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.full_name