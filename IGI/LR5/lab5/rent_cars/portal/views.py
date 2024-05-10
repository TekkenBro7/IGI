from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def privacy_policy(request):
    return render(request, 'portal/privacy_policy.html')

def about_company(request):
    return render(request, 'portal/about_company.html')