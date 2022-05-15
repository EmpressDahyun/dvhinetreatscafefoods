from asyncore import write
from dataclasses import field, fields
from django.contrib import admin
from pyparsing import Or
from .models import *
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id','recipient_name','phone_number','barangay','landmark','street_name')
    list_filter = ('barangay', 'phone_number')
    list_per_page = 10
    search_fields = ('recipient_name', 'barangay', 'landmark')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_editable = ('product',)
    list_filter = ('user', 'product')
    list_per_page = 10
    search_fields = ('user', 'product')

class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    pass
    list_display = ('user','address','total_price','remarks','order_date')

class OrderSlipAdmin(admin.ModelAdmin):
    list_display = ('invoice_no','file_upload')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'event_name', 'event_date', 'event_time', 'event_time_end' , 'status')
    list_editable = ('event_name', 'status')
    list_filter = ('status', 'event_date')
    list_per_page = 20
    search_fields = ('user__username', 'event_name')

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('description', 'image', 'upload_date')
    list_editable = ('image','image')
    list_filter = ('description', 'upload_date')
    list_per_page = 10
    search_fields = ('description', 'description')

admin.site.register(DeliveryInformation, DeliveryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRequest, OrderSlipAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Gallery, GalleryAdmin)
