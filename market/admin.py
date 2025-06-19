from django.contrib import admin

from .models import Image, ProductIndex, ProductClothing, CategoryClothing

admin.site.register(Image)
admin.site.register(ProductIndex)


@admin.register(CategoryClothing)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductClothing)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'in_stock', 'category']
    list_filter = ['in_stock', 'category']
    prepopulated_fields = {'slug': ('name',)}