from django.shortcuts import render, redirect
from cars.models import Car, BodyType, CarModel
from .forms import CarForm, CarModelForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from django.http import HttpResponse


def is_not_admin(user):
    return user.is_authenticated and not user.is_superuser


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin, login_url='home')
def car_create(request):
    if  request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'
    form = CarForm()
    return render(request, 'cars/car_create.html', {'form': form})


def car_list(request):
    model_type = request.GET.get('model_type', '')
    sort_by = request.GET.get('sort_by')
    body_type_id = request.GET.get('body_type')
    year = request.GET.get('year')
    year_filter = request.GET.get('greater_year')

    cars = Car.objects.all()
    body_types = BodyType.objects.all()
    
    if model_type:
        car_model = CarModel.objects.filter(name__icontains=model_type).first()
        if car_model:        
            cars = cars.filter(model=car_model)
        else:
            cars = []
    
    if body_type_id:
        cars = cars.filter(body_type_id=body_type_id)

    if year:
        cars = cars.filter(year=year)

    if year_filter:
        cars = cars.filter(year__gt=year_filter)

    if sort_by == 'name':
        cars = cars.order_by('model__name')
    elif sort_by == 'year':
        cars = cars.order_by('year')
    elif sort_by == 'cost':
        cars = cars.order_by('car_cost')

    context = {
        'body_types': body_types,
        'cars': cars,
        'model_type': model_type,
        'selected_body_type': body_type_id,
        'selected_year': year,
        'selected_sort_by': sort_by,
        'year_gt': year_filter
    }
    return render(request, 'cars/car_filter.html', context)


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_details.html'
    context_object_name = 'car'
    
 
@user_passes_test(is_admin, login_url='home')
def car_delete_view(request, pk):
    car = Car.objects.get(pk=pk)    
    if request.method == 'POST':
        car.delete()
        return redirect('home')    
    return render(request, 'cars/car_delete.html', {'car': car})
    
  
@user_passes_test(is_admin, login_url='home')
def car_update_view(request, pk):
    car = Car.objects.get(pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            current_datetime = timezone.now()
            car.updated_at = current_datetime        
            form.save()
            return redirect('car_detail', pk=pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_create.html', {'form': form})
    
    
@user_passes_test(is_admin, login_url='home')    
def add_car_model(request):
    if request.method == 'POST':
        form = CarModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarModelForm()
    
    context = {
        'form': form
    }
    return render(request, 'cars/car_model_create.html', context)


@user_passes_test(is_admin, login_url='home')
def car_model_list(request):
    car_models = CarModel.objects.all()
    context = {
        'car_models': car_models
    }
    return render(request, 'cars/car_model_list.html', context)


@user_passes_test(is_admin, login_url='home')
def delete_car_model(request, pk):
    car_model = CarModel.objects.get(pk=pk)
    car_model.delete()
    return redirect('car_model_list')