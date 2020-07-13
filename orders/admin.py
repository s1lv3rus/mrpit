import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment;' \
#                                       'filename={}.csv'.format(opts.verbose_name)
#     writer = csv.writer(response)
#
#     fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
#     # Write a first row with header information
#     writer.writerow([field.verbose_name for field in fields])
#     # Write data rows
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime('%d/%m/%Y')
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response
#
#
# export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['flavour']


#
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'client', 'first_name', 'last_name', 'email',
#                     'city', 'address', 'postal_code', 'phone', 'paid', 'deliver_cost',
#                     'created', 'status', 'comment', 'coupon', order_detail]
#     list_filter = ['paid', 'created', 'updated', 'status']
#     list_editable = ['status']
#     inlines = [OrderItemInline]
#

class ProductResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'city', 'address', 'postal_code', 'phone', 'paid',
                  'deliver_cost', 'get_total_cost', 'created', 'status', 'comment', 'coupon')


class OrderAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['id', 'city', 'paid', 'get_total_cost', 'deliver_cost',
                    'status', order_detail, 'track_number', 'comment', 'coupon', 'created']
    list_filter = ['paid', 'created', 'updated', 'status']
    list_editable = ['status', 'comment']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
