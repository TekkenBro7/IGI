from django import forms
from .models import Car, CarModel, BodyType

class CarForm(forms.ModelForm):      
    license_plate = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Номер машины'
            }
        )
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Модель'
            }
        )
    )
    body_type = forms.ModelChoiceField(
        queryset=BodyType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Тип кузова'
            }
        )
    )
    year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Year'
            }
        )
    )
    car_cost = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Car cost'
            }
        )
    )
    rental_cost_per_day = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Rental cost per day'
            }
        )
    )
 
    class Meta:
        model = Car
        exclude = ['created_at', 'updated_at']
        fields = '__all__'
        
        
        
class CarModelForm(forms.ModelForm):
    brand = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Бренд машины'
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Название машины'
            }
        )
    )
    
    class Meta:
        model = CarModel
        fields = ['name', 'brand']