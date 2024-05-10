from django.contrib import admin
from .models import BodyType, CarModel, Car, Discounts, Penalties, PromoCode, Rental

admin.site.register(BodyType)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Discounts)
admin.site.register(Penalties)
admin.site.register(PromoCode)
admin.site.register(Rental)