from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import User
        from core.models import Category, CategoryGroup
        default_categories = [category_group for category_group in CategoryGroup.objects.all()]
        for user in User.objects.all():
            for default_category in default_categories:
                for category in user.category_set.all():
                    if category.name == default_category.name and category.category_group == default_category:
                        break
                else:
                    Category.objects.create(name=default_category.name, category_group=default_category, user=user)
