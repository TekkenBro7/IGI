from .models import Review, Employee
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'photo', 'job_description', 'phone_number', 'email', 'url']
        widgets = {
            'job_description': forms.Textarea(),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Телефон'}),
            'url': forms.URLInput(attrs={'placeholder': 'URL информации о сотруднике'})
        }