
from django.utils import timezone
from django.db import models
from django.urls import reverse


class Image(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

class ProductIndex(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class CategoryClothing(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class ProductClothing(models.Model):
    category = models.ForeignKey(CategoryClothing, related_name='products', on_delete=models.CASCADE, verbose_name="Категория", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Рейтинг")
    reviews = models.PositiveIntegerField(default=0, verbose_name="Количество отзывов")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('market:shop-details', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"