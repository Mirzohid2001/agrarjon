from django.db import models
from users.models import User

# Create your models here.

AREA_CHOICES = (
    ("1-MINTAQA", "1-MINTAQA"),
    ("2-MINTAQA", "2-MINTAQA"),
    ("3-MINTAQA", "3-MINTAQA"),
)

REVIEW_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)


class Area(models.Model):
    name = models.CharField(max_length=255, choices=AREA_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'areas'
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.name


class Seed(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seeds'
        verbose_name = 'Семя'
        verbose_name_plural = 'Семена'

    def __str__(self):
        return self.name


class Tree(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trees'
        verbose_name = 'Дерево'
        verbose_name_plural = 'Деревья'

    def __str__(self):
        return self.name


class Oil(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oils'

    def __str__(self):
        return self.name

class WorkerTariff(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.FloatField()
    monthly_wage = models.IntegerField()
    daily_wage = models.FloatField()
    weekly_wage = models.FloatField()
    wage_with_coefficient = models.IntegerField()
    wage_for_7_hours = models.FloatField()

    class Meta:
        db_table = 'worker_tariffs'
        verbose_name = 'Тариф работника'
        verbose_name_plural = 'Тарифы работников'

    def __str__(self):
        return self.name


class TractorTariff(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.FloatField()
    monthly_wage = models.IntegerField()
    daily_wage = models.FloatField()
    weekly_wage = models.FloatField()
    wage_with_coefficient = models.IntegerField()
    wage_for_7_hours = models.FloatField()

    class Meta:
        db_table = 'tractor_tariffs'
        verbose_name = 'Тариф трактора'
        verbose_name_plural = 'Тарифы тракторов'

    def __str__(self):
        return self.name


class Tractor(models.Model):
    name = models.CharField(max_length=255)
    oil = models.ForeignKey(Oil, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, null=True, blank=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    tariffs = models.ManyToManyField(TractorTariff)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tractors'
        verbose_name = 'Трактор'
        verbose_name_plural = 'Тракторы'

    def __str__(self):
        return self.name


class Worker(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, null=True, blank=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, null=True, blank=True)
    tariffs = models.ManyToManyField(WorkerTariff)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workers'
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

class WorkerTariffAssignment(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    tariff = models.ForeignKey(WorkerTariff, on_delete=models.CASCADE)
    hours = models.IntegerField()

    class Meta:
        db_table = 'worker_tariff_assignments'
        verbose_name = 'Назначение тарифа работника'
        verbose_name_plural = 'Назначения тарифов работников'


class TractorTariffAssignment(models.Model):
    tractor = models.ForeignKey(Tractor, on_delete=models.CASCADE)
    tariff = models.ForeignKey(TractorTariff, on_delete=models.CASCADE)
    hours = models.IntegerField()

    class Meta:
        db_table = 'tractor_tariff_assignments'
        verbose_name = 'Назначение тарифа трактора'
        verbose_name_plural = 'Назначения тарифов тракторов'



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    excel_file = models.FileField(upload_to='excel_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Fertiliser(models.Model):
    name = models.CharField(max_length=255)
    price_per_kg = models.IntegerField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, null=True, blank=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fertilisers'
        verbose_name = 'Удобрение'
        verbose_name_plural = 'Удобрения'

    def __str__(self):
        return self.name


class WorkType(models.Model):
    name = models.CharField(max_length=255)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, null=True, blank=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, null=True, blank=True)
    worker_tariff = models.ForeignKey(WorkerTariff, on_delete=models.CASCADE, null=True, blank=True)
    tractor_tariff = models.ForeignKey(TractorTariff, on_delete=models.CASCADE, null=True, blank=True)
    hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'work_types'
        verbose_name = 'Тип работы'
        verbose_name_plural = 'Типы работы'

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Legal_Documents(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to='legal_documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Правовые документы'
        verbose_name_plural = 'Правовые документы'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.CharField(max_length=255, choices=REVIEW_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Banner(models.Model):
    image = models.ImageField(upload_to='banner_images/')
    text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Mems(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='mems_images/')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'
