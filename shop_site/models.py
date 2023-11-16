from django.db import models
from .mixins import *
from django.conf import settings
"""
Категории
    Имя
    Картинка
    Описание
Бренды
    Имя
    Картинка
    Описание
Продукты
    Имя
    Описание
    Главная картинка
    Цена
    Цвета
    Вес
    Штрих код продукта
    
Картинки-Продуктов
    Продукт
    Картинка


Блоги(новости)
    Тема
    Текст
    Картинка
    Дата создания
    Автор
Работники
    ФИО
    Должность
    Автарка
Отзывы
    ФИО
    Должность
    Сообщение
    Аватарка
Заявки
    Имя
    Фамилия
    Номер
    Почта
    Сообщение
Корзина(для клиентов)
    Пользователь
    Продукт
    Количество
"""

class Contacts(TimestampMixin, models.Model):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    number = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    message = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

class Workers(models.Model):
    fullname = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    avatar = models.ImageField()

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

class Reviews(models.Model):
    fullname = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    message = models.CharField(max_length=250)
    avatar = models.ImageField()

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Blogs(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Brands(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    image = models.ImageField()
    price = models.FloatField()
    color = models.CharField(max_length=250)
    weight = models.FloatField()
    barcode = models.CharField(max_length=250)
    categoryObject = models.ForeignKey(Category, on_delete=models.CASCADE)
    brandObject = models.ForeignKey(Brands, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class ProductsImages(models.Model):
    productObject = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField()

    class Meta:
        verbose_name = "Картинка-Продукта"
        verbose_name_plural = "Картинки-Продуктов"

class ProductsLikes(models.Model):
    productObject = models.ForeignKey(Products, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Лайк продукта"
        verbose_name_plural = "Лайки продуктов"

    
class ProductsRaitings(models.Model):
    productObject = models.ForeignKey(Products, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    points = models.IntegerField()

    class Meta:
        verbose_name = "Рейтинг продукта"
        verbose_name_plural = "Рейтинги продуктов"


class Subscriptions(models.Model):
    mail = models.TextField(max_length=255)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщении"

class ShoppingCart(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    productObject = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
