from django.db import models
from users.models import User


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    video = models.FileField(upload_to='company_videos/', null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    legal_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=20)
    bank_details = models.TextField()

    def __str__(self):
        return self.name
    
    
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    content = models.TextField()

    def __str__(self):
        return self.title


class FAQEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    job_description = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return self.user
    
    
class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.date}"