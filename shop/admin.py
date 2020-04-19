from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

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


# @admin.register(Flavour)
# class FlavourAdmin(admin.ModelAdmin):
#     list_display = ['name', 'product', 'supplier', 'quantity', 'for_offer']
#     list_filter = ['product', 'supplier', 'name', 'quantity']
#     list_editable = ['quantity', 'for_offer']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product", "author", "body", "date"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["name", 'date']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'calc', 'sorting']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['calc', 'sorting']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'size', 'price', 'available')


class FlavoursInLine(admin.StackedInline):
    model = Flavour
    raw_id_fields = ("product",)


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['name', 'size', 'supplier', 'category', 'subcategory', 'recommendation']
    list_filter = ['available', 'category', 'supplier', 'created', 'updated']
    list_editable = ['recommendation']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FlavoursInLine, ]


# для экспорта данных
class FlavourResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id')
    supplier = Field(attribute='product__supplier__name', column_name='Производитель')
    product = Field(attribute='product__name', column_name='Название товара')
    name = Field(attribute='name', column_name='Название вкуса')
    quantity = Field(attribute='quantity', column_name='Количество')
    purchase_price = Field(attribute='purchase_price', column_name='Закупочная цена')
    price = Field(attribute='price', column_name='Цена')
    price2 = Field(attribute='price2', column_name='Цена ранее')
    percent = Field(attribute='percent', column_name='Процент накрутки')
    for_offer = Field(attribute='for_offer', column_name='Для офера')

    class Meta:
        model = Flavour


# для отображения в админке
class FlavourAdmin(ImportExportModelAdmin):
    resource_class = FlavourResource
    list_display = ['id', 'supplier', 'product', 'name', 'size', 'quantity', 'purchase_price', 'price', 'price2',
                    'percent', 'for_offer']
    list_filter = ['product__supplier', 'product__category', 'product', 'name', 'quantity']
    list_editable = ['purchase_price', 'price', 'price2', 'quantity', 'for_offer']


admin.site.register(Flavour, FlavourAdmin)
admin.site.register(Product, ProductAdmin)
