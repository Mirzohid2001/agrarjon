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

    def save(self, *args, **kwargs):
        super(Area, self).save(*args, **kwargs)

    class Meta:
        db_table = 'areas'

    class Meta:
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

    def save(self, *args, **kwargs):
        super(Seed, self).save(*args, **kwargs)

    class Meta:
        db_table = 'seeds'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Семя'
        verbose_name_plural = 'Семена'

class Oil(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Oil, self).save(*args, **kwargs)

    class Meta:
        db_table = 'oils'


    def __str__(self):
        return self.name

class Tractor(models.Model):
    name = models.CharField(max_length=255)
    oil = models.ForeignKey(Oil, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    hour = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Tractor, self).save(*args, **kwargs)

    class Meta:
        db_table = 'tractors'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Трактор'
        verbose_name_plural = 'Тракторы'

class Worker(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    salary = models.IntegerField()
    hour = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Worker, self).save(*args, **kwargs)

    class Meta:
        db_table = 'workers'

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    excel_file = models.FileField(upload_to='excel_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    class Meta:
        db_table = 'orders'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Fertiliser(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Fertiliser, self).save(*args, **kwargs)

    class Meta:
        db_table = 'fertilisers'

    class Meta:
        verbose_name = 'Удобрение'
        verbose_name_plural = 'Удобрения'

    def __str__(self):
        return self.name

class WorkType(models.Model):
    name = models.CharField(max_length=255)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    traktor = models.ForeignKey(Tractor, on_delete=models.CASCADE)
    hour = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Тип работы'
        verbose_name_plural = 'Типы работы'

    def save(self, *args, **kwargs):
        super(WorkType, self).save(*args, **kwargs)

    class Meta:
        db_table = 'work_types'

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





