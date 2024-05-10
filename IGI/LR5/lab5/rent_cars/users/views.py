from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib import messages
from .forms import LoginForm, SignUpForm, PromoCodeForm, PenaltyForm, DiscountForm, RentalForm, RentalEditForm, SignUpEmpForm
from cars.models import BodyType, Car, Discounts, Penalties, PromoCode, Rental
from users.models import Customer, User
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta, date
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import calendar
import plotly.graph_objects as go
from calendar import HTMLCalendar
import re
from django.db.models import Sum, Avg, F, ExpressionWrapper, DateTimeField, Count
from statistics import mode, median, mean
from datetime import datetime
from django.http import HttpResponse
import logging
from cars.views import car_create

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')
# , format='%(asctime)s - %(levelname)s - %(message)s', filemode='w'




def index(request):
    
   # userr = User.objects.get(username='tekkenbro')
   # customer = Customer.objects.get(user=userr)
   # 
   # age = customer.age
   # return HttpResponse(age)
    
    
    cars = Car.objects.all()
    discounts = Discounts.objects.all()
    penalties = Penalties.objects.all()
    promoCodes = PromoCode.objects.all()
    sort_by_year = request.GET.get('sort_by_year')
    sort_by_cost = request.GET.get('sort_by_cost')
    sort_by_rental_cost = request.GET.get('sort_by_rental_cost')
    
    if sort_by_year == 'asc':
        cars = cars.order_by('year')
    elif sort_by_year == 'desc':
        cars = cars.order_by('-year')
    
    if sort_by_cost == 'asc':
        cars = cars.order_by('car_cost')
    elif sort_by_cost == 'desc':
        cars = cars.order_by('-car_cost')

    if sort_by_rental_cost == 'asc':
        cars = cars.order_by('rental_cost_per_day')
    elif sort_by_rental_cost == 'desc':
        cars = cars.order_by('-rental_cost_per_day')
    
    body_types = BodyType.objects.all()
    
    user_timezone=''
    current_date=''
    current_month = ''
    current_year = ''
    cal = ''
    month_number = ''
    
    if request.user.is_authenticated:
        user_timezone = timezone.get_current_timezone()
        current_date = timezone.localtime(timezone.now()).strftime('%d/%m/%Y')
        current_month = timezone.localtime(timezone.now()).month
        current_month = calendar.month_name[current_month]
        current_year = timezone.localtime(timezone.now()).year
        month_number = list(calendar.month_name).index(current_month)
        month_number = int(month_number)
        cal = HTMLCalendar().formatmonth(current_year, month_number)
    
        if  request.user.is_customer:
            customer = Customer.objects.get(user=request.user)
            num_rentals = Rental.objects.filter(client=customer).count()
            if num_rentals >= 3:
                customer.is_regular_customer = True
                customer.save()
    
    logging.info(f"Вызвана главная страница")
    
    return render(request, 'users/index.html', {'current_month': current_month, 'current_year': current_year, 'cal': cal, 'month_number': month_number, 'user_timezone': user_timezone, 'current_date': current_date, 'body_types': body_types, 'cars': cars, 'discounts': discounts, 'penalties': penalties, 'promoCodes': promoCodes})


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logging.info(" вошел в аккаунт")
                logging.info(f"{user.username} вошел в аккаунт")
                login_user(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('/')
            else:
                msg = 'invalid info'
                messages.success(request, "Ошибка, неправильный логин или пароль, повторите попытку!")
                return redirect('.')
               # return redirect('/')
        else:
            msg = 'error valid form'
        
    return render(request, 'users/login.html', {'form': form, 'msg': msg})

def calculate_age(birth_date: datetime):
    current_date = datetime.now().date()
    age = current_date.year - birth_date.year
    if current_date.month < birth_date.month or (current_date.month == birth_date.month and current_date.day < birth_date.day):
        age -= 1
    return age


def registration(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            address  = request.POST.get('address', '')
            telephone = request.POST.get('tel', '')
            PHONE_NUMBER_REGEX = r"^\+375(\s+)?\(?(17|29|33|44)\)?(\s+)?[0-9]{3}-[0-9]{2}-[0-9]{2}$"
            if not re.match(PHONE_NUMBER_REGEX, telephone):
                form.add_error('username', 'Некорректный формат телефонного номера')
                return render(request, 'users/registration.html', {'form': form, 'msg': 1})

            date_of_birth = form.cleaned_data.get('date_of_birth')
            user_age = calculate_age(date_of_birth)
            if user_age < 18:
                form.add_error('date_of_birth', 'Вам нет 18!')
                return render(request, 'users/registration.html', {'form': form, 'msg': 1})
            
            user.is_customer = True
            user.save()  
            Customer.objects.create(user=user, address=address, phone=telephone)
            logging.info(f"{user.username} зарегистрирован")         
            return redirect('/')
    logging.info(f"Вызвана страница регистрации")
    return render(request, 'users/registration.html', {'form': form, 'msg': 1})


def logoutUser(requset):
    logout(requset)
    logging.info(f"{requset.user.username} вышел с аккаунта")
    return redirect('home')

def is_not_admin(user):
    return user.is_authenticated and not user.is_superuser and not user.is_employee

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_worker(user):
    return user.is_authenticated and (user.is_superuser or user.is_employee)

def is_customer(user):
    return user.is_authenticated and user.is_customer

@user_passes_test(is_not_admin, login_url='home')
def rentCar(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            customer = Customer.objects.get(user=request.user)
            rental.client = customer           
            promocode = form.cleaned_data['promocode']
            
            rental_cost_per_day = rental.car.rental_cost_per_day
            rental_days = rental.rental_days
            total_amount = rental_cost_per_day * rental_days
            discount_percent_promo = 0         
            if promocode:     
                try:
                    promo_code = PromoCode.objects.get(code=promocode)
                    rental.promocode = promo_code         
                    rental_cost_per_day = rental.car.rental_cost_per_day
                    rental_days = rental.rental_days
                    total_amount = rental_cost_per_day * rental_days
                    discount_percent_promo = promo_code.discount_percentage             
                except ObjectDoesNotExist:
                    form.add_error('promocode', 'Промокод не найден.')
                    return render(request, 'users/rent_car.html', {'form': form})     
            if customer.is_firts_time:
                    try:
                        discount = Discounts.objects.get(name='Первая аренда')
                        discount_percent = discount.percentage
                        all_discount = discount_percent + discount_percent_promo
                        discounted_amount = total_amount - (total_amount * all_discount / 100)
                        rental.total_amount = discounted_amount
                        rental.discount = discount
                        customer.is_firts_time = False
                        customer.save()
                    except Discounts.DoesNotExist:
                        customer.is_firts_time = True
                        customer.save()          
            elif customer.is_regular_customer:
                    try:
                        discount = Discounts.objects.get(name='Постоянный клиент')
                        discount_percent = discount.percentage
                        all_discount = discount_percent + discount_percent_promo
                        discounted_amount = total_amount - (total_amount * all_discount / 100)
                        rental.total_amount = discounted_amount
                        rental.discount = discount
                    except Discounts.DoesNotExist:
                        request.user.is_regular_customer
            else:
                rental_cost_per_day = rental.car.rental_cost_per_day
                rental_days = rental.rental_days
                rental.total_amount = total_amount - (total_amount * discount_percent_promo / 100)
            
            rental_date = form.cleaned_data['rental_date']
            rental.rental_date = form.cleaned_data['rental_date']
            if rental_date < date.today():
                form.add_error('rental_date', 'Выберите дату, большую или равную текущей дате.')
                return render(request, 'users/rent_car.html', {'form': form})
            rental.expected_return_date = rental.rental_date + timedelta(days=rental_days)
            
            logging.info(f"Создан заказ для {customer.user.username}")
            
            rental.save()
            form.save_m2m()  # Сохраняем многие ко многим поля
            return redirect('home')
    else:
        form = RentalForm()
    return render(request, 'users/rent_car.html', {'form': form})

@user_passes_test(is_admin, login_url='home')
def add_employee(request):
    form = SignUpEmpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            
            date_of_birth = form.cleaned_data.get('date_of_birth')
            user_age = calculate_age(date_of_birth)
            if user_age < 18:
                form.add_error('date_of_birth', 'Вам нет 18!')
                return render(request, 'users/registration.html', {'form': form, 'msg': 1})               
            user.is_employee = True
            user.save()
            logging.info(f"Создан работник {user.username}")  
            return redirect('/')
    return render(request, 'users/registration.html', {'form': form})
    
    
def all_items(request):
    penalties = Penalties.objects.all()
    promo_codes = PromoCode.objects.all()
    discounts = Discounts.objects.all()
    logging.info(f"Вызвана страница всех бонусов")  
    return render(request, 'users/all_items.html', {'penalties': penalties, 'promo_codes': promo_codes, 'discounts': discounts})


@user_passes_test(is_admin, login_url='home')
def discount_add(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            percentage = int(form.cleaned_data['percentage'])
            if percentage < 0 or percentage > 100:
                form.add_error('percentage', 'Percentage must be between 0 and 100')
            else:
                form.save()
                logging.info(f"Скидка добавлена")  
                return redirect('all_items')
    else:
        form = DiscountForm()
    return render(request, 'users/discount_add.html', {'form': form})


@user_passes_test(is_admin, login_url='home')
def discount_edit(request, pk):
    discount = Discounts.objects.get(pk=pk)
    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            percentage = int(form.cleaned_data['percentage'])
            if percentage < 0 or percentage > 100:
                form.add_error('percentage', 'Percentage must be between 0 and 100')
            else:
                form.save()
                logging.info(f"Скидка изменена")  
                return redirect('all_items')
    else:
        form = DiscountForm(instance=discount)
    return render(request, 'users/discount_add.html', {'form': form})


@user_passes_test(is_admin, login_url='home')
def discount_delete(request, pk):
    discount = Discounts.objects.get(pk=pk)
    discount.delete()
    logging.info(f"Скидка удалена")  
    return redirect('all_items')


@user_passes_test(is_admin, login_url='home')
def promocode_add(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            if form.is_valid():
                discount_percentage = int(form.cleaned_data['discount_percentage'])
                if discount_percentage < 0 or discount_percentage > 100:
                    form.add_error('discount_percentage', 'Percentage must be between 0 and 100')
                else:
                    form.save()
                    logging.info(f"Промокод добавлена")  
                    return redirect('all_items')
    else:
        form = PromoCodeForm()
    return render(request, 'users/promocode_add.html', {'form': form})


@user_passes_test(is_admin, login_url='home')
def promocode_edit(request, pk):
    promocode = PromoCode.objects.get(pk=pk)
    if request.method == 'POST':
        form = PromoCodeForm(request.POST, instance=promocode)
        if form.is_valid():
            discount_percentage = int(form.cleaned_data['discount_percentage'])
            if discount_percentage < 0 or discount_percentage > 100:
                form.add_error('discount_percentage', 'Percentage must be between 0 and 100')
            else:
                form.save()
                logging.info(f"Промокод изменен")  
                return redirect('all_items')
    else:
        form = PromoCodeForm(instance=promocode)
    return render(request, 'users/promocode_add.html', {'form': form})


@user_passes_test(is_admin, login_url='home')
def promocode_delete(request, pk):
    promocode = PromoCode.objects.get(pk=pk)
    promocode.delete()
    logging.info(f"Промокод удален")  
    return redirect('all_items')


@user_passes_test(is_admin, login_url='home')
def penalty_add(request):
    if request.method == 'POST':
        form = PenaltyForm(request.POST)
        if form.is_valid():
            percentage = int(form.cleaned_data['percentage'])
            if percentage < 0 or percentage > 100:
                form.add_error('percentage', 'Percentage must be between 0 and 100')
            else:
                form.save()
                logging.info(f"Штраф добавлен")  
                return redirect('all_items')
    else:
        form = PenaltyForm()
    return render(request, 'users/penalty_add.html', {'form': form})


@user_passes_test(is_admin, login_url='home')
def penalty_edit(request, pk):
    penalty = Penalties.objects.get(pk=pk)
    if request.method == 'POST':
        form = PenaltyForm(request.POST, instance=penalty)
        if form.is_valid():
            percentage = int(form.cleaned_data['percentage'])
            if percentage < 0 or percentage > 100:
                form.add_error('percentage', 'Percentage must be between 0 and 100')
            else:
                form.save()
                logging.info(f"Штраф изменен")  
                return redirect('all_items')
    else:
        form = PenaltyForm(instance=penalty)
    return render(request, 'users/penalty_add.html', {'form': form})


@user_passes_test(is_admin, login_url='home')
def penalty_delete(request, pk):
    penalty = Penalties.objects.get(pk=pk)
    penalty.delete()
    logging.info(f"Штраф удален")  
    return redirect('all_items')

@user_passes_test(is_customer, login_url='home')
def user_rentals(request):
    current_user = request.user
    customer = Customer.objects.get(user=current_user)
    rentals = Rental.objects.filter(client=customer)
    logging.info(f"Вызвана страница заказов")  
    return render(request, 'users/profile.html', {'rentals': rentals})


@user_passes_test(is_worker, login_url='home')   
def filter_rentals(request):
    search_name = request.GET.get('search_name', '')
    search_car_id = request.GET.get('car_type')
    search_days = request.GET.get('search_days')
    search_promocode = request.GET.get('discount')
    sort_by = request.GET.get('sort_by')
    
    rentals = Rental.objects.all()
    cars = Car.objects.all()

    if search_name:
        rentals = rentals.filter(client__user__username__icontains=search_name)
    if search_car_id:
        rentals = rentals.filter(car_id=search_car_id)
    if search_days:
        rentals = rentals.filter(rental_days__gte=search_days)
    if search_promocode == "True":
        rentals = rentals.filter(promocode__isnull=False)
    elif search_promocode == "False":
        rentals = rentals.exclude(promocode__isnull=False)


    if sort_by == "name":
        rentals = rentals.order_by('-car__model')
    elif sort_by == "days":
        rentals = rentals.order_by('-rental_days')
    elif sort_by == "amount":
        rentals = rentals.order_by('-total_amount')

    context = {
        'filtered_rentals': rentals,
        'car_types': cars
        }
    logging.info(f"Вызвана страница фильтрации заказов")
    return render(request, 'users/filler_rentals.html', context)

@user_passes_test(is_worker, login_url='home')   
def rental_details(request, rental_id):
    rental = Rental.objects.get(pk=rental_id)
    context = {
        'rental': rental
    }  
    logging.info(f"Вызвана страница деталей заказа")  
    return render(request, 'users/rental_details.html', context)


@user_passes_test(is_worker, login_url='home')   
def delete_rental(request, rental_id):
        rental = Rental.objects.get(id=rental_id)
        rental.delete()
        logging.info(f"Заказ удален")
        return redirect('filter_rentals')
    

@user_passes_test(is_worker, login_url='home')    
def edit_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    zxc = rental.rental_days
    if request.method == 'POST':
        form = RentalEditForm(request.POST, instance=rental)
        if form.is_valid():
            rental_days = form.cleaned_data['rental_days']
            if rental_days < zxc:
                form.add_error('rental_days', 'Новое количество дней должно быть >= текущему значению')
            else:             
                delta_time = rental_days - zxc
                rental.expected_return_date = rental.expected_return_date + timedelta(days=delta_time)
                rental.total_amount += delta_time * rental.car.rental_cost_per_day

                previously_applied_penalties = rental.penalty.all()          
                penalties = form.cleaned_data.get('penalty')
                if penalties and not rental.is_pass:
                    new_penalties = [penalty for penalty in penalties if penalty not in previously_applied_penalties]
                    penalty_percentage = sum([penalty.percentage for penalty in new_penalties ])
                    rental.total_amount += (rental.total_amount * penalty_percentage) / 100         
                form.save()
                logging.info(f"Заказ изменен")
                return redirect('rental_details', rental.id)
    else:
        form = RentalEditForm(instance=rental)
    
    return render(request, 'users/edit_rental.html', {'form': form, 'rental': rental})


@user_passes_test(is_worker, login_url='home') 
def client_list(request):
    clients = Customer.objects.all()
    employees = User.objects.filter(is_employee=True)
    logging.info(f"Вызвана страница списка людей")
    return render(request, 'users/client.html', {'clients': clients, 'employees': employees})


@user_passes_test(is_worker, login_url='home') 
def rental_chart_view(request):
    rentals = Rental.objects.all()
    rental_dates = [rental.rental_date for rental in rentals]
    total_amounts = [rental.total_amount for rental in rentals]
    fig = go.Figure(data=[go.Bar(x=rental_dates, y=total_amounts)])
    
    fig.update_layout(
    title="Все аренды",
    xaxis_title="Даты аренды",
    yaxis_title="Цена"
    )
    
    plot_div = fig.to_html(full_html=False)
    
    clients = Customer.objects.order_by('user__username')

    # Общая сумма продаж
    total_sales = Rental.objects.aggregate(total_sales=Sum('total_amount'))['total_sales']

    # Среднее значение суммы продаж
    average_sales = Rental.objects.aggregate(average_sales=Avg('total_amount'))['average_sales']
    
    # Мода суммы продаж
    sales_list = Rental.objects.values_list('total_amount', flat=True)
    sales_mode = mode(sales_list)

    # Медиана суммы продаж
    sales_median = median(sales_list)
    
    # Подсчет количества аренд по типу товара
    popular_types = Rental.objects.values('car__model__name').annotate(rental_count=Count('car__model__name')).order_by('-rental_count')
    most_popular_type = popular_types.first()
    model_name = most_popular_type['car__model__name']
    rental_count = most_popular_type['rental_count']

    # Подсчет суммы продаж по типу товара
    profitable_types = Rental.objects.values('car__model__name').annotate(total_sales=Sum('total_amount')).order_by('-total_sales')

    # Тип товара с наибольшей прибылью
    most_profitable_type = profitable_types.first()['car__model__name']
    
    context = {
        'most_profitable_type': most_profitable_type,
        'rental_count': rental_count,
        'model_name': model_name,
        'sales_median': sales_median,
        'sales_mode': sales_mode,
        'clients': clients,
        'total_sales': total_sales,
        'average_sales': average_sales,
        'plot_div': plot_div
    }
    logging.info(f"Вызвана страница анализа заказов")
    return render(request, 'users/rental_chart.html', context=context)

