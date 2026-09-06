from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from .models import (
    Client, Car, Mechanic, Service, Part, 
    RepairOrder, OrderService, OrderPart
)


class ClientAPITestCase(TestCase):
    """Тесты для API клиентов"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.client_data = {
            'first_name': 'Иван',
            'last_name': 'Петров',
            'phone': '+79991234567',
            'email': 'ivan@test.ru'
        }
        self.client_obj = Client.objects.create(**self.client_data)

    def test_create_client(self):
        """Тест создания клиента (POST /api/clients/)"""
        data = {
            'first_name': 'Петр',
            'last_name': 'Сидоров',
            'phone': '+79998765432',
            'email': 'petr@test.ru'
        }
        response = self.client_api.post('/api/clients/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Петр')
        self.assertEqual(Client.objects.count(), 2)

    def test_get_clients_list(self):
        """Тест получения списка клиентов (GET /api/clients/)"""
        response = self.client_api.get('/api/clients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Исправлено: обращаемся к response.data напрямую (это список)
        self.assertEqual(len(response.data), 1)

    def test_get_client_detail(self):
        """Тест получения одного клиента (GET /api/clients/{id}/)"""
        response = self.client_api.get(f'/api/clients/{self.client_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Иван')
        self.assertEqual(response.data['last_name'], 'Петров')

    def test_update_client(self):
        """Тест обновления клиента (PUT /api/clients/{id}/)"""
        data = {'first_name': 'Иван Обновленный'}
        response = self.client_api.patch(
            f'/api/clients/{self.client_obj.id}/', 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Иван Обновленный')

    def test_delete_client(self):
        """Тест удаления клиента (DELETE /api/clients/{id}/)"""
        response = self.client_api.delete(f'/api/clients/{self.client_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)


class CarAPITestCase(TestCase):
    """Тесты для API автомобилей"""
    
    def setUp(self):
        self.client_api = APIClient()
        # Сначала создаем клиента (объект)
        self.client_obj = Client.objects.create(
            first_name='Иван',
            last_name='Петров',
            phone='+79991234567'
        )
        # Теперь передаем объект клиента, а не ID
        self.car_data = {
            'client': self.client_obj,  # ← Исправлено: передаем объект, а не ID
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'license_plate': 'А123ВС77',
            'vin': 'JTDBE32K000000001'
        }
        self.car_obj = Car.objects.create(**self.car_data)

    def test_create_car(self):
        """Тест создания автомобиля (POST /api/cars/)"""
        data = {
            'client': self.client_obj.id,  # ← Для API нужен ID
            'brand': 'BMW',
            'model': 'X5',
            'year': 2021,
            'license_plate': 'В456МК77',
            'vin': 'JTDBE32K000000002'
        }
        response = self.client_api.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['brand'], 'BMW')
        self.assertEqual(Car.objects.count(), 2)

    def test_get_cars_list(self):
        """Тест получения списка автомобилей (GET /api/cars/)"""
        response = self.client_api.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Исправлено: response.data - это список
        self.assertEqual(len(response.data), 1)

    def test_get_car_detail(self):
        """Тест получения одного автомобиля (GET /api/cars/{id}/)"""
        response = self.client_api.get(f'/api/cars/{self.car_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], 'Toyota')
        self.assertEqual(response.data['license_plate'], 'А123ВС77')

    def test_update_car(self):
        """Тест обновления автомобиля (PUT /api/cars/{id}/)"""
        data = {'license_plate': 'B123TT77'}
        response = self.client_api.patch(
            f'/api/cars/{self.car_obj.id}/', 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['license_plate'], 'B123TT77')

    def test_delete_car(self):
        """Тест удаления автомобиля (DELETE /api/cars/{id}/)"""
        response = self.client_api.delete(f'/api/cars/{self.car_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)


class MechanicAPITestCase(TestCase):
    """Тесты для API мастеров"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.mechanic_data = {
            'first_name': 'Сергей',
            'last_name': 'Иванов',
            'phone': '+79991112233',
            'specialization': 'Механик',
            'hire_date': '2020-01-01'
        }
        self.mechanic_obj = Mechanic.objects.create(**self.mechanic_data)

    def test_create_mechanic(self):
        """Тест создания мастера (POST /api/mechanics/)"""
        data = {
            'first_name': 'Алексей',
            'last_name': 'Смирнов',
            'phone': '+79992223344',
            'specialization': 'Электрик',
            'hire_date': '2021-03-15'
        }
        response = self.client_api.post('/api/mechanics/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Алексей')
        self.assertEqual(Mechanic.objects.count(), 2)

    def test_get_mechanics_list(self):
        """Тест получения списка мастеров (GET /api/mechanics/)"""
        response = self.client_api.get('/api/mechanics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_mechanic_detail(self):
        """Тест получения одного мастера (GET /api/mechanics/{id}/)"""
        response = self.client_api.get(f'/api/mechanics/{self.mechanic_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Сергей')

    def test_update_mechanic(self):
        """Тест обновления мастера (PUT /api/mechanics/{id}/)"""
        data = {'specialization': 'Главный механик'}
        response = self.client_api.patch(
            f'/api/mechanics/{self.mechanic_obj.id}/', 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialization'], 'Главный механик')

    def test_delete_mechanic(self):
        """Тест удаления мастера (DELETE /api/mechanics/{id}/)"""
        response = self.client_api.delete(f'/api/mechanics/{self.mechanic_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mechanic.objects.count(), 0)


class ServiceAPITestCase(TestCase):
    """Тесты для API услуг"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.service_data = {
            'name': 'Замена масла',
            'description': 'Замена моторного масла с фильтром',
            'price': 2500.00,
            'duration': 60
        }
        self.service_obj = Service.objects.create(**self.service_data)

    def test_create_service(self):
        """Тест создания услуги (POST /api/services/)"""
        data = {
            'name': 'Диагностика двигателя',
            'description': 'Полная компьютерная диагностика',
            'price': 1500.00,
            'duration': 30
        }
        response = self.client_api.post('/api/services/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Диагностика двигателя')
        self.assertEqual(Service.objects.count(), 2)

    def test_get_services_list(self):
        """Тест получения списка услуг (GET /api/services/)"""
        response = self.client_api.get('/api/services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_service_detail(self):
        """Тест получения одной услуги (GET /api/services/{id}/)"""
        response = self.client_api.get(f'/api/services/{self.service_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Замена масла')

    def test_update_service(self):
        """Тест обновления услуги (PUT /api/services/{id}/)"""
        data = {'price': 2800.00}
        response = self.client_api.patch(
            f'/api/services/{self.service_obj.id}/', 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), 2800.00)

    def test_delete_service(self):
        """Тест удаления услуги (DELETE /api/services/{id}/)"""
        response = self.client_api.delete(f'/api/services/{self.service_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 0)


class PartAPITestCase(TestCase):
    """Тесты для API запчастей"""
    
    def setUp(self):
        self.client_api = APIClient()
        self.part_data = {
            'name': 'Масляный фильтр',
            'article': 'MF-001',
            'price': 800.00,
            'quantity': 15
        }
        self.part_obj = Part.objects.create(**self.part_data)

    def test_create_part(self):
        """Тест создания запчасти (POST /api/parts/)"""
        data = {
            'name': 'Тормозные колодки',
            'article': 'BP-002',
            'price': 2500.00,
            'quantity': 8
        }
        response = self.client_api.post('/api/parts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Тормозные колодки')
        self.assertEqual(Part.objects.count(), 2)

    def test_get_parts_list(self):
        """Тест получения списка запчастей (GET /api/parts/)"""
        response = self.client_api.get('/api/parts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_part_detail(self):
        """Тест получения одной запчасти (GET /api/parts/{id}/)"""
        response = self.client_api.get(f'/api/parts/{self.part_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Масляный фильтр')

    def test_update_part(self):
        """Тест обновления запчасти (PUT /api/parts/{id}/)"""
        data = {'quantity': 20}
        response = self.client_api.patch(
            f'/api/parts/{self.part_obj.id}/', 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 20)

    def test_delete_part(self):
        """Тест удаления запчасти (DELETE /api/parts/{id}/)"""
        response = self.client_api.delete(f'/api/parts/{self.part_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Part.objects.count(), 0)


class RepairOrderAPITestCase(TestCase):
    """Тесты для API заказов-нарядов"""
    
    def setUp(self):
        self.client_api = APIClient()
        
        # Создаем клиента
        self.client_obj = Client.objects.create(
            first_name='Иван',
            last_name='Петров',
            phone='+79991234567'
        )
        
        # Создаем автомобиль (передаем объект клиента)
        self.car = Car.objects.create(
            client=self.client_obj,  # ← Исправлено: передаем объект
            brand='Toyota',
            model='Camry',
            year=2020,
            license_plate='А123ВС77',
            vin='JTDBE32K000000001'
        )
        
        # Создаем мастера
        self.mechanic = Mechanic.objects.create(
            first_name='Сергей',
            last_name='Иванов',
            phone='+79991112233',
            specialization='Механик',
            hire_date='2020-01-01'
        )
        
        # Создаем услугу
        self.service = Service.objects.create(
            name='Замена масла',
            price=2500.00,
            duration=60
        )
        
        # Создаем заказ
        self.order = RepairOrder.objects.create(
            car=self.car,
            mechanic=self.mechanic,
            description='Плановое ТО',
            planned_date='2024-12-01T10:00:00Z'
        )

    def test_create_order(self):
        """Тест создания заказа (POST /api/orders/)"""
        data = {
            'car': self.car.id,
            'mechanic': self.mechanic.id,
            'description': 'Срочный ремонт',
            'planned_date': '2024-12-05T10:00:00Z',
            'status': 'NEW'
        }
        response = self.client_api.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'Срочный ремонт')
        self.assertEqual(RepairOrder.objects.count(), 2)

    def test_get_orders_list(self):
        """Тест получения списка заказов (GET /api/orders/)"""
        response = self.client_api.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Исправлено: response.data - это список
        self.assertEqual(len(response.data), 1)

    def test_get_order_detail(self):
        """Тест получения одного заказа (GET /api/orders/{id}/)"""
        response = self.client_api.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Плановое ТО')

    def test_update_order_status(self):
        """Тест обновления статуса заказа (PUT /api/orders/{id}/)"""
        data = {'status': 'IN_PROGRESS'}
        response = self.client_api.patch(
            f'/api/orders/{self.order.id}/', 
            data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'IN_PROGRESS')

    def test_delete_order(self):
        """Тест удаления заказа (DELETE /api/orders/{id}/)"""
        response = self.client_api.delete(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RepairOrder.objects.count(), 0)