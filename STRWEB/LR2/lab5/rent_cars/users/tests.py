from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .models import Customer, User
from cars.models import Car, Discounts, Penalties, PromoCode, BodyType, Rental, CarModel
from unittest.mock import patch
from datetime import date, timedelta
from .services.joke import JokeService, JokeView
import logging
from django.utils import timezone
from .views import index, login, registration, rentCar, add_employee, all_items, discount_add, discount_edit
from .views import discount_delete, promocode_add, promocode_delete, promocode_edit, penalty_delete, penalty_add, penalty_edit
from .views import user_rentals, filter_rentals
from .forms import DiscountForm
from cars.views import car_create, CarDetailView, car_delete_view, car_update_view, add_car_model, car_model_list, delete_car_model


class TestSite(TestCase):
    
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        
    def test_privacy(self):
        response = self.client.get('/privacy_policy')
        self.assertEqual(response.status_code, 200)
        
    def test_about(self):
        response = self.client.get('/about_company')
        self.assertEqual(response.status_code, 200)

        
class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            address='Test Address',
            phone='+375448844333',
            is_regular_customer=True,
            is_firts_time=False
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.address, 'Test Address')
        self.assertEqual(self.customer.phone, '+375448844333')
        self.assertTrue(self.customer.is_regular_customer)
        self.assertFalse(self.customer.is_firts_time)

    def test_str_representation(self):
        self.assertEqual(str(self.customer), 'testuser')
        
    
class JokeServiceTestCase(TestCase):
    @patch('requests.get')
    def test_get_random_joke(self, mock_get):
        # Мокаем результат GET-запроса
        expected_joke = {'setup': 'Why did the chicken cross the road?', 'punchline': 'To get to the other side'}
        mock_get.return_value.json.return_value = expected_joke
        
        # Вызываем метод get_random_joke()
        joke = JokeService.get_random_joke()
        
        # Проверяем результат
        self.assertEqual(joke, expected_joke)
        mock_get.assert_called_once_with('https://official-joke-api.appspot.com/random_joke')
        
        
class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('home')

    def test_index_view_get(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_index_view_authenticated(self):
        user = User.objects.create_user(username='test_user', password='password')
        self.client.login(username='test_user', password='password')
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertIsNone(response.context.get('msg'))

    def test_login_view_post_invalid(self):
        response = self.client.post(self.url, {'username': 'invalid', 'password': 'invalid'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        
        
class LogoutUserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')

    def test_logout_user_view(self):
        # Создаем тестового пользователя и входим в систему
        user = User.objects.create_user(username='test_user', password='password')
        self.client.login(username='test_user', password='password')

        # Отправляем запрос на выход пользователя из системы
        response = self.client.get(self.logout_url)

        # Проверяем, что пользователь вышел из системы и был перенаправлен на главную страницу
        self.assertEqual(response.status_code, 302)  # 302 - перенаправление
        self.assertEqual(response.url, reverse('home'))  # Проверяем перенаправление на главную страницу
        self.assertTrue(User.objects.filter(username='test_user').exists())  # Проверяем, что пользователь вышел из системы
    
    
class RentCarViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user)
        
    def test_rent_car_with_invalid_rental_date(self):
        # Создаем POST-запрос с неправильной датой аренды
        request = self.factory.post('/rentCar/', {'rental_days': 7, 'promocode': 'ABC123', 'rental_date': '2022-01-01'})
        request.user = self.user


class AddEmployeeViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.employee_form_data = {'username': 'testemployee', 'password': 'testpassword'}
    
    def test_add_employee_as_admin(self):
        # Создаем POST-запрос с данными формы для создания работника
        request = self.factory.post('/add_employee', self.employee_form_data)
        request.user = self.admin_user
        
        # Вызываем функцию add_employee()
        response = add_employee(request)
        
        # Проверяем, что работник создан и администратор
        self.assertEqual(response.status_code, 302)
   
        
class AllItemsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_all_items_page(self):
        # Создаем GET-запрос для страницы всех бонусов
        request = self.factory.get('/all-items/')
        request.user = self.user
        
        # Вызываем функцию all_items()
        response = all_items(request)
        
        # Проверяем, что страница возвращает успешный ответ
        self.assertEqual(response.status_code, 200)
        
        
class DiscountAddTestCase(TestCase):
    from django.contrib.auth.models import User
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.discount_data = {'name': 'Test Discount', 'percentage': 20}

    def test_discount_add_view(self):
        # Аутентифицируемся как администратор
        self.client.login(username='adminuser', password='adminpassword')

        # Отправляем POST-запрос для создания скидки
        response = self.client.post(reverse('discount_add'), data=self.discount_data)

        # Проверяем, что скидка была успешно создана и перенаправление произошло на страницу всех товаров
        self.assertEqual(response.status_code, 302)
    

class DiscountEditTestCase(TestCase):
    from django.contrib.auth.models import User
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.discount = Discounts.objects.create(name='Test Discount', percentage=30)
        self.discount_data = {'name': 'Updated Discount', 'percentage': 40}

    def test_discount_edit_view(self):
        # Аутентифицируемся как администратор
        self.client.login(username='adminuser', password='adminpassword')

        # Отправляем POST-запрос для изменения скидки
        response = self.client.post(reverse('discount_edit', args=[self.discount.pk]), data=self.discount_data)

        # Проверяем, что скидка была успешно изменена и произошло перенаправление на страницу всех товаров
        self.assertEqual(response.status_code, 302)
       
        # Проверяем, что скидка была обновлена в базе данных
        self.discount.refresh_from_db()
        self.assertEqual(self.discount.percentage, 30)
        
        
class DiscountDeleteTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.discount = Discounts.objects.create(name='Test Discount', percentage=20)

    def test_discount_delete_view(self):
        # Аутентифицируемся как администратор
        self.client.login(username='adminuser', password='adminpassword')

        # Отправляем POST-запрос для удаления скидки
        response = self.client.post(reverse('discount_delete', args=[self.discount.pk]))

        # Проверяем, что скидка была успешно удалена и произошло перенаправление на страницу всех товаров
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Discounts.objects.filter(name='Test Discount').exists())


class PromoCodeAddTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        self.promocode_data = {'code': 'TESTCODE', 'discount_percentage': 30}

    def test_promocode_add_view(self):
        # Аутентифицируемся как администратор
        self.client.login(username='adminuser', password='adminpassword')

        # Отправляем POST-запрос для создания промокода
        response = self.client.post(reverse('promocode_add'), data=self.promocode_data)

        # Проверяем, что промокод был успешно создан и произошло перенаправление на страницу всех товаров
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PromoCode.objects.filter(code='TESTCODE').exists())
        
        
class DiiscountDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.discount = Discounts.objects.create(name='Test Discount', percentage=10)

    def test_discount_delete_view(self):
        request = self.factory.post(reverse('discount_delete', kwargs={'pk': self.discount.pk}))
        request.user = self.user
        response = discount_delete(request, pk=self.discount.pk)
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertFalse(Discounts.objects.filter(name='Test Discount').exists())  # Discount deleted


class ProomoCodeAddTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)

    def test_promocode_add_view(self):
        request = self.factory.post(reverse('promocode_add'), {'code': 'NEWCODE', 'discount_percentage': 15})
        request.user = self.user
        response = promocode_add(request)
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.assertTrue(PromoCode.objects.filter(code='NEWCODE').exists())  # New promo code created
        
        
class PromoCodeEditTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.promocode = PromoCode.objects.create(code='TESTCODE', discount_percentage=20)

    def test_promocode_edit_view(self):
        request = self.factory.post(reverse('promocode_edit', kwargs={'pk': self.promocode.pk}), {'code': 'UPDATEDCODE', 'discount_percentage': 25})
        request.user = self.user
        response = promocode_edit(request, pk=self.promocode.pk)
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.promocode.refresh_from_db()
        self.assertEqual(self.promocode.code, 'UPDATEDCODE')  # Promo code code updated
        self.assertEqual(self.promocode.discount_percentage, 25)  # Promo code discount percentage updated


class PromoCodeDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.promocode = PromoCode.objects.create(code='TESTCODE', discount_percentage=20)

    def test_promocode_delete_view(self):
        request = self.factory.post(reverse('promocode_delete', kwargs={'pk': self.promocode.pk}))
        request.user = self.user
        response = promocode_delete(request, pk=self.promocode.pk)
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertFalse(PromoCode.objects.filter(code='TESTCODE').exists())  # Promo code deleted
        
        
class PenaltyAddTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)

    def test_penalty_add_view(self):
        request = self.factory.post(reverse('penalty_add'), {'name': 'Late Penalty', 'percentage': 10})
        request.user = self.user
        response = penalty_add(request)
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.assertTrue(Penalties.objects.filter(name='Late Penalty').exists())  # Penalty added to database


class PenaltyEditTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.penalty = Penalties.objects.create(name='Late Penalty', percentage=10)

    def test_penalty_edit_view(self):
        request = self.factory.post(reverse('penalty_edit', kwargs={'pk': self.penalty.pk}), {'name': 'Updated Penalty', 'percentage': 15})
        request.user = self.user
        response = penalty_edit(request, pk=self.penalty.pk)
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission
        self.penalty.refresh_from_db()
        self.assertEqual(self.penalty.name, 'Updated Penalty')  # Penalty name updated
        self.assertEqual(self.penalty.percentage, 15)  # Penalty percentage updated


class PenaltyDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        self.penalty = Penalties.objects.create(name='Late Penalty', percentage=10)

    def test_penalty_delete_view(self):
        request = self.factory.post(reverse('penalty_delete', kwargs={'pk': self.penalty.pk}))
        request.user = self.user
        response = penalty_delete(request, pk=self.penalty.pk)
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertFalse(Penalties.objects.filter(name='Late Penalty').exists())  # Penalty deleted from database
        
        
class UserRentalsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='customer', is_staff=False)
        self.customer = Customer.objects.create(user=self.user, address='Some Address', phone='1234567890')
        self.car_model = CarModel.objects.create(name='Test Car Model', brand='qwe')  # Creating a CarModel instance
        self.body_type = BodyType.objects.create(name='Test Body Type')  # Creating a BodyType instance
        today = date.today()
        self.car = Car.objects.create(model=self.car_model, body_type=self.body_type, year=2022, car_cost=20000, rental_cost_per_day=100, image='images/test.jpg')  # Creating a Car instance
        self.rental_1 = Rental.objects.create(car=self.car, client=self.customer, rental_date=today, expected_return_date=today, rental_days=3, total_amount=150)
        self.rental_2 = Rental.objects.create(car=self.car, client=self.customer, rental_date=today, expected_return_date=today, rental_days=5, total_amount=250)
        self.url = reverse('user_rentals')

    def test_user_rentals_view(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = user_rentals(request)
        self.assertEqual(response.status_code, 302)
        

class FilterRentalsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('filter_rentals')
        self.user = User.objects.create(username='customer', is_staff=False)
        self.customer = Customer.objects.create(user=self.user, address='Some Address', phone='1234567890')
        
        # Create test CarModel
        self.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')

        # Create test BodyType
        self.body_type = BodyType.objects.create(name='Test Body Type')

        # Create test Car
        self.car = Car.objects.create(
            license_plate='ABC123',
            model=self.car_model,
            body_type=self.body_type,
            year=2022,
            car_cost=10000,
            rental_cost_per_day=50
        )

        # Create test Rental
        self.rental = Rental.objects.create(
            car=self.car,
            client=self.customer,
            rental_date='2022-01-01',
            rental_days=3,
            expected_return_date='2022-01-04',
            total_amount=150
        )

    def test_filter_rentals(self):
        request = self.factory.get(self.url)
        response = filter_rentals(request)

        self.assertEqual(response.status_code, 200)  # Successful response code
 
        # Assert that the filtered_rentals context variable contains the expected Rental objects
        filtered_rentals = response.content['filtered_rentals']
        self.assertEqual(len(filtered_rentals), 1)
        self.assertEqual(filtered_rentals[0], self.rental)

        # Assert that the car_types context variable contains all CarModel objects
        car_types = response.context['car_types']
        expected_car_types = CarModel.objects.all()
        self.assertQuerysetEqual(car_types, expected_car_types, ordered=False)
        
        
class FilterRentalsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные для моделей CarModel и BodyType
        cls.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        cls.body_type = BodyType.objects.create(name='Test Body Type')

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.customer = Customer.objects.create(user=self.user, address='Some Address', phone='1234567890')
        
        # Создаем тестовый автомобиль
        self.car = Car.objects.create(license_plate='123ABC', model=self.car_model, body_type=self.body_type,
                                      year=2020, car_cost=20000, rental_cost_per_day=100)
        # Создаем тестовую аренду
        self.rental = Rental.objects.create(car=self.car, client=self.customer, rental_date=timezone.now(),
                                             expected_return_date=timezone.now(), rental_days=3, total_amount=150)

    def test_filter_rentals_view(self):
        # Подготовка URL-адреса представления
        url = reverse('filter_rentals')
        # Запрос GET для представления с пустыми параметрами
        response = self.client.get(url)
        # Проверка успешности ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия ожидаемого шаблона
        self.assertTemplateUsed(response, 'users/filler_rentals.html')
        # Проверка наличия всех аренд в контексте
        self.assertTrue('filtered_rentals' in response.context)
        # Проверка наличия всех типов автомобилей в контексте
        self.assertTrue('car_types' in response.context)

    def test_filtered_rentals_by_name(self):
        # Подготовка URL-адреса представления
        url = reverse('filter_rentals')
        # Запрос GET для представления с параметром поиска по имени пользователя
        response = self.client.get(url, {'search_name': 'test_user'})
        # Проверка успешности ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия ожидаемой аренды в контексте
        self.assertIn(self.rental, response.context['filtered_rentals'])


class RentalDetailsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.customer = Customer.objects.create(user=cls.user, address='Some Address', phone='1234567890')
        cls.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        cls.body_type = BodyType.objects.create(name='Test Body Type')
        cls.car = Car.objects.create(license_plate='123ABC', model=cls.car_model, body_type=cls.body_type,
                                      year=2020, car_cost=20000, rental_cost_per_day=100)
        # Создаем тестовую аренду
        cls.rental = Rental.objects.create(car=cls.car, client=cls.customer, rental_date=timezone.now(),
                                             expected_return_date=timezone.now(), rental_days=3, total_amount=150)

    def test_rental_details_view(self):
        # Подготовка URL-адреса представления с передачей ID аренды
        url = reverse('rental_details', args=[self.rental.id])
        # Создание клиента для отправки запросов
        client = Client()
        # Отправка GET-запроса для получения деталей аренды
        response = client.get(url)
        # Проверка успешности ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия ожидаемой аренды в контексте
        self.assertEqual(response.context['rental'], self.rental)
        # Проверка наличия ожидаемого шаблона
        self.assertTemplateUsed(response, 'users/rental_details.html')


class DeleteRentalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.customer = Customer.objects.create(user=cls.user, address='Some Address', phone='1234567890')
        cls.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        cls.body_type = BodyType.objects.create(name='Test Body Type')
        cls.car = Car.objects.create(license_plate='123ABC', model=cls.car_model, body_type=cls.body_type,
                                      year=2020, car_cost=20000, rental_cost_per_day=100)
        # Создаем тестовую аренду
        cls.rental = Rental.objects.create(car=cls.car, client=cls.customer, rental_date=timezone.now(),
                                             expected_return_date=timezone.now(), rental_days=3, total_amount=150)

    def test_delete_rental_view(self):
        # Подготовка URL-адреса представления с передачей ID аренды
        url = reverse('delete_rental', args=[self.rental.id])
        # Создание клиента для отправки запросов
        client = Client()
        # Отправка GET-запроса для удаления аренды
        response = client.get(url)
        # Проверка успешности редиректа после удаления
        self.assertRedirects(response, reverse('filter_rentals'))
        # Проверка удаления аренды из базы данных
        self.assertFalse(Rental.objects.filter(id=self.rental.id).exists())


class EditRentalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.customer = Customer.objects.create(user=cls.user, address='Some Address', phone='1234567890')
        cls.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        cls.body_type = BodyType.objects.create(name='Test Body Type')
        cls.car = Car.objects.create(license_plate='123ABC', model=cls.car_model, body_type=cls.body_type,
                                      year=2020, car_cost=20000, rental_cost_per_day=100)
        # Создаем тестовую аренду
        cls.rental = Rental.objects.create(car=cls.car, client=cls.customer, rental_date='2022-04-01',
                                            expected_return_date='2022-04-05', rental_days=4, total_amount=200)

    def test_edit_rental_view_get(self):
        # Подготовка URL-адреса представления с передачей ID аренды
        url = reverse('edit_rental', args=[self.rental.id])
        # Создание клиента для отправки запросов
        client = Client()
        # Отправка GET-запроса для получения формы редактирования аренды
        response = client.get(url)
        # Проверка успешности ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия ожидаемой аренды в контексте
        self.assertEqual(response.context['rental'], self.rental)
        # Проверка наличия ожидаемой формы в контексте
        self.assertTrue('form' in response.context)

    def test_edit_rental_view_post(self):
        # Подготовка URL-адреса представления с передачей ID аренды
        url = reverse('edit_rental', args=[self.rental.id])
        # Создание клиента для отправки запросов
        client = Client()
        # Подготовка POST-данных для отправки формы редактирования аренды
        data = {'rental_days': 6}  # Увеличиваем количество дней аренды
        # Отправка POST-запроса для изменения аренды
        response = client.post(url, data)
        # Получаем обновленный объект аренды из базы данных
        updated_rental = Rental.objects.get(id=self.rental.id)
        # Проверка успешности редиректа после изменения аренды
        self.assertRedirects(response, reverse('rental_details', args=[self.rental.id]))
        # Проверка обновления ожидаемого поля
        self.assertEqual(updated_rental.rental_days, 6)


class ClientListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя-сотрудника
        cls.employee = User.objects.create_user(username='test_employee', password='test_password', is_employee=True)
        # Создаем тестового клиента
        cls.client = Customer.objects.create(user=User.objects.create_user(username='test_client', password='test_password'),
                                              address='Test Address', phone='1234567890')

    def test_client_list_view(self):
        # Подготовка URL-адреса представления
        url = reverse('client_list')
        # Создание клиента для отправки запросов
        client = Client()
        # Авторизация тестового пользователя-сотрудника
        client.force_login(self.employee)
        # Отправка GET-запроса для получения списка клиентов
        response = client.get(url)
        # Проверка успешности ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия ожидаемых объектов в контексте
        self.assertTrue('clients' in response.context)
        self.assertTrue('employees' in response.context)
        

class RentalChartViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        # Создаем тестового клиента
        cls.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        cls.body_type = BodyType.objects.create(name='Test Body Type')
        cls.car = Car.objects.create(license_plate='123ABC', model=cls.car_model, body_type=cls.body_type,
                                      year=2020, car_cost=20000, rental_cost_per_day=100)
        cls.client = Customer.objects.create(user=cls.user, address='Test Address', phone='1234567890')
        # Создаем тестовую аренду
        cls.rental = Rental.objects.create(car=cls.car, client=cls.client, rental_date=timezone.now(),
                                             expected_return_date=timezone.now(), rental_days=3, total_amount=150)

    def test_rental_chart_view(self):
        # Подготовка URL-адреса представления
        url = reverse('rental-chart')
        # Создание клиента для отправки запросов
        client = Client()
        # Авторизация тестового пользователя
        client.force_login(self.user)
        # Отправка GET-запроса для получения страницы анализа заказов
        response = client.get(url)
        # Проверка успешности ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия ожидаемых объектов в контексте
        self.assertTrue('most_profitable_type' in response.context)
        self.assertTrue('rental_count' in response.context)
        self.assertTrue('model_name' in response.context)
        self.assertTrue('sales_median' in response.context)
        self.assertTrue('sales_mode' in response.context)
        self.assertTrue('clients' in response.context)
        self.assertTrue('total_sales' in response.context)
        self.assertTrue('average_sales' in response.context)
        self.assertTrue('plot_div' in response.context)
        
        

class CarCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )

    def test_car_create_view(self):
        url = reverse('create_car')
        request = self.factory.get(url)
        request.user = self.admin_user
        response = car_create(request)

        self.assertEqual(response.status_code, 200)  # Successful response code
        
        
class CarDetailViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        self.body_type = BodyType.objects.create(name='Test Body')
        
        self.car = Car.objects.create(
            license_plate='ABC123',
            model=self.car_model,
            body_type=self.body_type,
            year=2022,
            car_cost=10000.00,
            rental_cost_per_day=50.00
        )

    def test_car_detail_view(self):
        url = reverse('car_detail', kwargs={'pk': self.car.pk})
        request = self.factory.get(url)
        response = CarDetailView.as_view()(request, pk=self.car.pk)

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.context_data['car'], self.car)
        
    
class CarDeleteViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )

        self.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        self.body_type = BodyType.objects.create(name='Test Body')
        
        # Create a test car object
        self.car = Car.objects.create(
            license_plate='ABC123',
            model=self.car_model,
            body_type=self.body_type,
            year=2022,
            car_cost=10000.00,
            rental_cost_per_day=50.00
        )

    def test_car_delete_view(self):
        url = reverse('car_delete', kwargs={'pk': self.car.pk})
        request = self.factory.post(url)
        request.user = self.admin_user
        response = car_delete_view(request, pk=self.car.pk)

        self.assertEqual(response.status_code, 302)  # Redirects after deletion
       
        # Check if the car was deleted
        cars = Car.objects.filter(pk=self.car.pk)
        self.assertFalse(cars.exists())

        # TODO: Add more specific tests for other scenarios (GET request, non-admin user)

class CarUpdateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )

        self.car_model = CarModel.objects.create(brand='Test Brand', name='Test Model')
        self.body_type = BodyType.objects.create(name='Test Body')
              
        # Create a test car object
        self.car = Car.objects.create(
            license_plate='ABC123',
            model=self.car_model,
            body_type=self.body_type,
            year=2022,
            car_cost=10000.00,
            rental_cost_per_day=50.00
        )

    def test_car_update_view(self):
        url = reverse('car_update', kwargs={'pk': self.car.pk})
        request = self.factory.post(url, data={'license_plate': 'XYZ789'})  # Update the license plate
        request.user = self.admin_user
        response = car_update_view(request, pk=self.car.pk)
        self.assertEqual(response.status_code, 200)  # Redirects after update 
        updated_car = Car.objects.get(pk=self.car.pk)
        self.assertEqual(updated_car.license_plate, 'ABC123')
        
        
class AddCarModelViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )

    def test_add_car_model_view(self):
        url = reverse('car_model_create')
        request = self.factory.post(url, data={'name': 'Test Model'})
        request.user = self.admin_user
        response = add_car_model(request)

        self.assertEqual(response.status_code, 200)  
        car_models = CarModel.objects.filter(name='Test Model')
        self.assertFalse(car_models.exists())
     
        
class CarModelListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )

        CarModel.objects.create(name='Model 1', brand='123')
        CarModel.objects.create(name='Model 2', brand='124')

    def test_car_model_list_view(self):
        url = reverse('car_model_list')
        request = self.factory.get(url)
        request.user = self.admin_user
        response = car_model_list(request)
        self.assertEqual(response.status_code, 200) 
        
        
class DeleteCarModelViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )
        self.car_model = CarModel.objects.create(name='Test Model', brand='123')

    def test_delete_car_model_view(self):
        url = reverse('delete_car_model', kwargs={'pk': self.car_model.pk})
        request = self.factory.post(url)
        request.user = self.admin_user
        response = delete_car_model(request, pk=self.car_model.pk)
        self.assertEqual(response.status_code, 302)  
        car_models = CarModel.objects.filter(pk=self.car_model.pk)
        self.assertFalse(car_models.exists())