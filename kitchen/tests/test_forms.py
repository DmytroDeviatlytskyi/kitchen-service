from django.test import TestCase

from kitchen.forms import (
    CookCreationForm,
    CookSearchForm,
    CookExperienceUpdateForm,
    DishTypeSearchForm,
    IngredientSearchForm,
    DishForm,
    DishSearchForm,
)
from kitchen.models import DishType, Cook, Ingredient


class CookFormTest(TestCase):
    def test_cook_form_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 4,
        }
        form = CookCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"]
        )

    def test_cook_search_form_is_valid(self):
        form_data = {
            "username": "test_username"
        }
        form = CookSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )


class CookExperienceUpdateFormTest(TestCase):
    def test_cook_experience_update_form_is_valid(self):
        form_data = {
            "years_of_experience": 1
        }
        form = CookExperienceUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["years_of_experience"],
            form_data["years_of_experience"]
        )


class DishTypeFormTest(TestCase):
    def test_dish_type_search_form_is_valid(self):
        form_data = {
            "name": "test_dish_type"
        }
        form = DishTypeSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            form_data["name"]
        )
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )


class IngredientFormTest(TestCase):
    def test_ingredient_search_form_is_valid(self):
        form_data = {
            "name": "test_ingredient"
        }
        form = IngredientSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            form_data["name"]
        )
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )


class DishFormTest(TestCase):
    def test_dish_form_is_valid(self):
        dish_type = DishType.objects.create(name="Test type")
        cook = Cook.objects.create_user(
            username="Test Cook",
            password="test1234",
            years_of_experience=1,
        )
        ingredient = Ingredient.objects.create(
            name="Test ingredient"
        )
        form_data = {
            "name": "Test dish",
            "description": "Test description",
            "price": 15,
            "type": dish_type.id,
            "cooks": [cook.id, ],
            "ingredients": [ingredient.id, ],
        }
        form = DishForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            form_data["name"]
        )
        self.assertEqual(
            form.cleaned_data["type"],
            dish_type
        )
        self.assertTrue(
            cook in form.cleaned_data["cooks"]
        )
        self.assertTrue(
            ingredient in form.cleaned_data["ingredients"]
        )

    def test_dish_search_form_is_valid(self):
        form_data = {
            "name": "test_dish"
        }
        form = DishSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            form_data["name"]
        )
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )
