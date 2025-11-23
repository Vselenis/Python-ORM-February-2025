from django.core.exceptions import ValidationError
from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class ZooKeeper(Employee):


    class Specialities(models.TextChoices):
        MAMMALS = 'Mammals', 'Mammals'
        BIRDS = 'Birds', 'Birds'
        REPTILE = 'Reptiles', 'Reptiles'
        OTHERS = 'others', 'others'

    specialty = models.CharField(choices=Specialities.choices, max_length=50)
    managed_animals = models.ManyToManyField(Animal)

    def clean(self):
        if self.specialty not in self.Specialities.choices:
            raise ValidationError('Specialty must be a valid choice')

class Veterinarian(Employee):
    licence_number = models.CharField(max_length=10)




class ZooDisplayAnimal(Animal):

    class Meta:
        proxy = True

