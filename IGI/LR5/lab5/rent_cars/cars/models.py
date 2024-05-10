from django.db import models
from users.models import Customer
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class CarModel(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BodyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

    
class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    car_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rental_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', default='images/no.jpg', verbose_name="Загрузите аватар для машины")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.model.name

    def get_absolute_url(self):
        return f'/car/{self.id}'
    
    
class Discounts(models.Model):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.IntegerField()

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_percentage = models.IntegerField()

    def __str__(self):
        return self.code


class Penalties(models.Model):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.IntegerField()

    def __str__(self):
        return self.name


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rental_date = models.DateField()
    rental_days = models.PositiveIntegerField()
    expected_return_date = models.DateField()
    total_amount = models.PositiveIntegerField()
    promocode = models.ForeignKey(PromoCode, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discounts, on_delete=models.CASCADE, null=True, blank=True)
    penalty = models.ManyToManyField(Penalties, null=True, blank=True)
    is_pass = models.BooleanField('is_pass', default=False)


    def __str__(self):
        return f"{self.car} - {self.client}"