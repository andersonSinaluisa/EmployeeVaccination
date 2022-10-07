from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    identification = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    birth_date = models.DateField(null=True)
    address = models.CharField(max_length=255,null=True)
    is_vaccinated = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'


class Vaccine(models.Model):
    type = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)



class Vaccination(models.Model):
    type = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    number_doses = models.IntegerField()
    date = models.DateField()
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True)