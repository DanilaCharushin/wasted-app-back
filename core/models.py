from django.contrib.auth.models import User as BaseUser
from django.db import models


class CategoryGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")

    class Meta:
        verbose_name = "Группа категорий"
        verbose_name_plural = "Группы категорий"


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    category_group = models.ForeignKey(
        CategoryGroup,
        verbose_name="Группа категории",
        on_delete=models.CASCADE,
    )
