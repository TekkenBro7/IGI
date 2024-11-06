from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Company, NewsArticle, FAQEntry, Employee, Vacancy, Review
from .forms import ReviewForm, EmployeeForm
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import RegexValidator
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import User
# Create your views here.

def privacy_policy(request):
    return render(request, 'portal/privacy_policy.html')

def about_company(request):
    company = Company.objects.first()
    return render(request, 'portal/about_company.html', {'company': company})

def all_news(request):
    articles = NewsArticle.objects.all().order_by('time_create')
    return render(request, 'portal/news.html', {'articles': articles})

def news_details(request, pk):
    article = NewsArticle.objects.get(pk=pk)
    return render(request, 'portal/news_detail.html', {'article': article})

def faq_list(request):
    faqs = FAQEntry.objects.all().order_by('-date_added')
    return render(request, 'portal/faq.html', {'faqs': faqs})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'portal/employee_list.html', {'employees': employees})

def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'portal/vacancy_list.html', {'vacancies': vacancies})


def allreviews(request):
    reviews = Review.objects.all().order_by('-date')
    return render(request, 'portal/reviews.html', {'reviews': reviews})

def is_customer(user):
    return user.is_authenticated and user.is_customer

@user_passes_test(is_customer, login_url='reviews')
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')  
    else:
        form = ReviewForm()
    return render(request, 'portal/add_review.html', {'form': form})


def employee_list_table(request):
    employees = Employee.objects.all()
    
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_list_table')  # перенаправление на страницу списка сотрудников
    else:
        form = EmployeeForm()

    return render(request, 'portal/employee_list_table.html', 
                  {
                      'employees': employees,
                      'form': form
                  })
    
