from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kitchen.models import Cook, Dish, DishType, Ingredient


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience", )}), )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "type", )
    search_fields = ("name", )
    list_filter = ("type", )


admin.site.register(DishType)
admin.site.register(Ingredient)
