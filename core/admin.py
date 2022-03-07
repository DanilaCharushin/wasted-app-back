from django.contrib import admin

from .models import Category, CategoryGroup, Waste


@admin.register(CategoryGroup)
class CategoryGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    pass
