from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    """Клиент автосервиса"""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    """Автомобиль клиента"""
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='cars',
        verbose_name='Клиент'
    )
    brand = models.CharField('Марка', max_length=50)
    model = models.CharField('Модель', max_length=50)
    year = models.PositiveIntegerField('Год выпуска', validators=[MinValueValidator(1900), MaxValueValidator(2026)])
    license_plate = models.CharField('Госномер', max_length=15, unique=True)
    vin = models.CharField('VIN-номер', max_length=17, unique=True, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['brand', 'model']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Mechanic(models.Model):
    """Мастер автосервиса"""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    specialization = models.CharField('Специализация', max_length=200)
    hire_date = models.DateField('Дата приема')
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.specialization})"


class Service(models.Model):
    """Услуга автосервиса"""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.PositiveIntegerField('Длительность (мин)', default=60)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price} ₽"


class Part(models.Model):
    """Запчасть"""
    name = models.CharField('Название', max_length=200)
    article = models.CharField('Артикул', max_length=50, unique=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField('Количество на складе', default=0)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (арт. {self.article})"


class RepairOrder(models.Model):
    """Заказ-наряд на ремонт"""
    STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('IN_PROGRESS', 'В работе'),
        ('COMPLETED', 'Завершен'),
        ('CANCELLED', 'Отменен'),
    ]
    
    car = models.ForeignKey(
        Car, 
        on_delete=models.PROTECT, 
        related_name='orders',
        verbose_name='Автомобиль'
    )
    mechanic = models.ForeignKey(
        Mechanic, 
        on_delete=models.PROTECT, 
        related_name='orders',
        verbose_name='Мастер'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='NEW')
    description = models.TextField('Описание работ', blank=True)
    planned_date = models.DateTimeField('Плановая дата выполнения')
    completed_date = models.DateTimeField('Дата завершения', null=True, blank=True)
    total_cost = models.DecimalField('Итоговая стоимость', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ-наряд'
        verbose_name_plural = 'Заказы-наряды'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.car}"


class OrderService(models.Model):
    """Услуги в заказе (промежуточная таблица)"""
    order = models.ForeignKey(
        RepairOrder, 
        on_delete=models.CASCADE, 
        related_name='order_services',
        verbose_name='Заказ'
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.PROTECT, 
        related_name='order_services',
        verbose_name='Услуга'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена за единицу', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Услуга в заказе'
        verbose_name_plural = 'Услуги в заказе'
        unique_together = ['order', 'service']

    def __str__(self):
        return f"{self.order} - {self.service} x{self.quantity}"


class OrderPart(models.Model):
    """Запчасти в заказе (промежуточная таблица)"""
    order = models.ForeignKey(
        RepairOrder, 
        on_delete=models.CASCADE, 
        related_name='order_parts',
        verbose_name='Заказ'
    )
    part = models.ForeignKey(
        Part, 
        on_delete=models.PROTECT, 
        related_name='order_parts',
        verbose_name='Запчасть'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена за единицу', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Запчасть в заказе'
        verbose_name_plural = 'Запчасти в заказе'
        unique_together = ['order', 'part']

    def __str__(self):
        return f"{self.order} - {self.part} x{self.quantity}"