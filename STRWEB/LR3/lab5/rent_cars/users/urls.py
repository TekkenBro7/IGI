"""
URL configuration for rent_cars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
import portal.views
import cars.views

from .services.joke import JokeView
from .services.nationality import nationalize

urlpatterns = [
    path('', views.index, name='home'),       
    re_path(r'^joke/$', JokeView.as_view(), name='joke'),
    re_path(r'^nationalize/$', nationalize, name='nationalize'),
    re_path(r'^rental-chart/$', views.rental_chart_view, name='rental-chart'),re_path(r'^login/$', views.login, name='login'),
    re_path(r'^registration/$', views.registration, name='reg'),
    re_path(r'^logout/$', views.logoutUser, name='logout'),
    re_path(r'^all-items/$', views.all_items, name='all_items'),
    re_path(r'^user_rentals/$', views.user_rentals, name='user_rentals'),path('filter_rentals/', views.filter_rentals, name='filter_rentals'),
    re_path(r'^rental/(?P<rental_id>\d+)/$', views.rental_details, name='rental_details'),
    re_path(r'^rental/(?P<rental_id>\d+)/delete/$', views.delete_rental, name='delete_rental'),
    re_path(r'^rental/(?P<rental_id>\d+)/edit/$', views.edit_rental, name='edit_rental'),
    re_path(r'^client_list/$', views.client_list, name='client_list'),
    re_path(r'^rentCar/$', views.rentCar, name='zxc'),
    re_path(r'^add_employee/$', views.add_employee, name='add_employee'),re_path(r'^discounts/add/$', views.discount_add, name='discount_add'),
    re_path(r'^discounts/(?P<pk>\d+)/edit/$', views.discount_edit, name='discount_edit'),
    re_path(r'^discounts/(?P<pk>\d+)/delete/$', views.discount_delete, name='discount_delete'),   
    re_path(r'^promocode/add/$', views.promocode_add, name="promocode_add"),
    re_path(r'^promocode/(?P<pk>\d+)/edit/$', views.promocode_edit, name="promocode_edit"),
    re_path(r'^promocode/(?P<pk>\d+)/delete/$', views.promocode_delete, name="promocode_delete"),
    re_path(r'^penalty/add/$', views.penalty_add, name="penalty_add"),
    re_path(r'^penalty/(?P<pk>\d+)/edit/$', views.penalty_edit, name="penalty_edit"),
    re_path(r'^penalty/(?P<pk>\d+)/delete/$', views.penalty_delete, name="penalty_delete"),
    path('create_car', cars.views.car_create, name='create_car'),  # для админа создание машины
    path('car/<int:pk>', cars.views.CarDetailView.as_view(), name='car_detail'),
    path('car/<int:pk>/update', cars.views.car_update_view, name='car_update'),  # для админа изменение машины
    path('car/<int:pk>/delete', cars.views.car_delete_view, name='car_delete'),  # для админа удаление машины
    path("car_model_create", cars.views.add_car_model, name="car_model_create"),  # для админа создание модели авто
    path("car_model_list", cars.views.car_model_list, name="car_model_list"),
    path('car_model_list/delete/<int:pk>', cars.views.delete_car_model, name='delete_car_model'), # для админа удаления модели
    path('car_filter', cars.views.car_list, name='car_filter'),
     
    
    path('privacy_policy', portal.views.privacy_policy, name='privacy_policy'),
    path('about_company', portal.views.about_company, name='about_company'),
    path('news', portal.views.all_news, name='news'),
    path('news/<int:pk>/', portal.views.news_details, name='news_details'),
    path('faq/', portal.views.faq_list, name='faq_list'),
    path('employees/', portal.views.employee_list, name='employee_list'),
    path('vacancies/', portal.views.vacancy_list, name='vacancy_list'),
    path('reviews', portal.views.allreviews, name='reviews'),
    path('reviews/add/', portal.views.add_review, name='add_review'),
    
    path('add_to_cart/<int:car_id>/', cars.views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('order/<int:car_id>/', views.order_car_view, name='order_car'),
    
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    
    path('task7_prot/', views.task7_prot, name='task7_prot'),
    path('task7_class/', views.task7_class, name='task7_class'),
    
    path('employee_list_table/', portal.views.employee_list_table, name='employee_list_table'),
    
    path('api/rentals-per-model/', views.rentals_per_model, name='rentals_per_model'),
]
# для подключения всех статических файлов
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)