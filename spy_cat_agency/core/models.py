from django.db import models
from django.core.exceptions import ValidationError
import requests

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    breed = models.CharField(max_length=100)
    salary = models.FloatField()

    def clean(self):
        response = requests.get(f"https://api.thecatapi.com/v1/breeds/{self.breed}") # Validate cat breed
        if response.status_code != 200:
            raise ValidationError(f"Breed '{self.breed}' didn`t exist in TheCatAPI.")

    def __str__(self):
        return self.name

class Mission(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    spy_cat = models.ForeignKey(SpyCat, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='in_progress')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission for {self.spy_cat.name}"

class Target(models.Model):
    mission = models.ForeignKey(Mission, related_name='targets', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name