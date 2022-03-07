from django.contrib.auth.models import User, User as BaseUser
from django.db import models


class CategoryGroup(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название", unique=True)

    def __str__(self):
        return f"<Группа категорий '{self.name}'>"

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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        db_index=True,
    )

    def __str__(self):
        return f"<Категория '{self.name}', {self.category_group.name} user {self.user.email}>"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Waste(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    amount = models.FloatField(verbose_name="Сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        db_index=True,
    )

    def __str__(self):
        return f"<Трата '{self.name}' - {self.amount} user {self.user.email}>"

    class Meta:
        verbose_name = "Трата"
        verbose_name_plural = "Траты"
