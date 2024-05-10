from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer
from cars.models import PromoCode, Discounts, Penalties, Rental, Car


class LoginForm(forms.Form):
    #  класс Meta не требуется, так как вы не используете модель для создания формы.
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите почту'
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }
        )
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth') #, #'address', 'phone', )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
   
     


class SignUpEmpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите почту'
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }
        )
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth')
     #   fields = ('username', 'password1', 'password2')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
     
class DiscountForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Название скидки'
            }
        )
    )
    percentage = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Процент скидки'
            }
        )
    )
    class Meta:
        model = Discounts
        fields = ['name', 'percentage']    


class PromoCodeForm(forms.ModelForm):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Код промокода'
            }
        )
    )
    discount_percentage = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Процент скидки'
            }
        )
    )
    class Meta:
        model = PromoCode
        fields = ['code', 'discount_percentage']


class PenaltyForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Название штрафа'
            }
        )
    )
    percentage = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Процент штрафа'
            }
        )
    )
    class Meta:
        model = Penalties
        fields = ['name', 'percentage']

        
class RentalForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Тип машины'
            }
        )
    )
    rental_days = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Количество дней'
            }
        )
    )
    promocode = forms.CharField(
        required=False,  # Делаем поле необязательным
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Промокод'
            }
        )
    )
    class Meta:
        model = Rental
        fields = ['car', 'rental_date', 'rental_days'] #'promocode']
        widgets = {
            'rental_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
        
class RentalEditForm(forms.ModelForm):
    rental_days = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Количество дней'
            }
        )
    )
    class Meta:
        model = Rental
        fields = ['rental_days', 'is_pass', 'penalty']
