from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'position']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['position']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'supplier', 'category', 'subcategory', 'price', 'price2', 'available',
                    'recommendation']
    list_filter = ['available', 'category', 'supplier', 'created', 'updated']
    list_editable = ['price', 'price2', 'available', 'recommendation']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Flavour)
class FlavourAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'supplier', 'quantity', 'for_offer']
    list_filter = ['product', 'name', 'quantity']
    list_editable = ['quantity', 'for_offer']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product", "author", "body", "date"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'calc']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['calc']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

