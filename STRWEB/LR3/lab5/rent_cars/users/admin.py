from django.contrib import admin
from .models import User, Customer, Partner, SliderSettings

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Partner)
admin.site.register(SliderSettings)