from django.contrib import admin
from .models import FooterContentModel, HomePageContentModel, MainCompanyModel, GroupModel, CompanyModel, StoreAddressModel, StoreGalleryModel


@admin.register(MainCompanyModel)
class MainCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'contact_email', 'contact_phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('title', 'description', 'contact_email')


@admin.register(GroupModel)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('name', 'description')


@admin.register(CompanyModel)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'group', 'description', 'is_active', 'created_at')
    list_filter = ('group', 'is_active', 'is_deleted')
    search_fields = ('title', 'description')


@admin.register(StoreAddressModel)
class StoreAddressAdmin(admin.ModelAdmin):
    list_display = ('company', 'address', 'opening_hours', 'email', 'phone', 'capacity', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('address', 'email', 'phone')

@admin.register(StoreGalleryModel)
class StoreGalleryModelAdmin(admin.ModelAdmin):
    list_display = ('store', 'images')
    list_filter = ('is_active', 'is_deleted')

@admin.register(HomePageContentModel)
class HomePageContentModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')

@admin.register(FooterContentModel)
class FooterContentModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')