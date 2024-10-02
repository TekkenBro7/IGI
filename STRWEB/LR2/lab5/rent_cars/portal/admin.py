from django.contrib import admin
from .models import Company, NewsArticle, FAQEntry, Employee, Vacancy, Review

# Register your models here.
admin.site.register(Company)
admin.site.register(NewsArticle)
admin.site.register(FAQEntry)
admin.site.register(Employee)
admin.site.register(Vacancy)
admin.site.register(Review)