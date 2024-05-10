from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps
from datetime import date

class User(AbstractUser):
    is_admin = models.BooleanField('is_admin', default=False)
    is_customer = models.BooleanField('is_customer', default=False)
    is_employee = models.BooleanField('is_employee', default=False)
    date_of_birth = models.DateField('date_of_birth', null=True, blank=True)
    
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    is_regular_customer = models.BooleanField('is_regular_customer', default=False)
    is_firts_time = models.BooleanField('is_firts_time', default=True)

    @property
    def age(self):
        if self.user.date_of_birth:
            today = date.today()
            age = today.year - self.user.date_of_birth.year
            if today.month < self.user.date_of_birth.month or (today.month == self.user.date_of_birth.month and today.day < self.user.date_of_birth.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return f"{self.user.username}"