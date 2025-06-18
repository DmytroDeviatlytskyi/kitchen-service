from django.test import TestCase
from django.urls import reverse

from kitchen.models import Cook, DishType, Ingredient, Dish


class CookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cook.objects.create_user(
            username="test",
            password="test123",
            years_of_experience=4,
        )

    def test_create_cook(self):
        cook = Cook.objects.get(id=1)
        self.assertEqual(cook.username, "test")
        self.assertTrue(cook.check_password("test123"))
        self.assertEqual(cook.years_of_experience, 4)

    def test_cook_str(self):
        cook = Cook.objects.get(id=1)
        expected_str = f"{cook.username}: ({cook.first_name} {cook.last_name})"
        self.assertEqual(str(cook), expected_str)

    def test_cook_get_absolute_url(self):
        cook = Cook.objects.get(id=1)
        expected = reverse("kitchen:cook-detail", kwargs={"pk": cook.pk})
        self.assertEqual(cook.get_absolute_url(), expected)


class DishTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DishType.objects.create(
            name="test_dish_type"
        )

    def test_create_dish_type(self):
        dish_type = DishType.objects.get(id=1)
        self.assertEqual(dish_type.name, "test_dish_type")

    def test_dish_type_str(self):
        dish_type = DishType.objects.get(id=1)
        self.assertEqual(str(dish_type), dish_type.name)


class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(
            name="test_ingredient"
        )

    def test_create_ingredient(self):
        ingredient = Ingredient.objects.get(id=1)
        self.assertEqual(ingredient.name, "test_ingredient")

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.get(id=1)
        self.assertEqual(str(ingredient), ingredient.name)


class DishModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cook.objects.create_user(
            username="test",
            password="test123",
            years_of_experience=4,
        )
        Ingredient.objects.create(
            name="test_ingredient",
        )
        test_dish_type = DishType.objects.create(
            name="test_dish_type"
        )
        test_dish = Dish.objects.create(
            name="test_dish",
            description="test-description",
            price=15,
            type=test_dish_type,
        )
        cooks = Cook.objects.all()
        ingredients = Ingredient.objects.all()
        test_dish.cooks.set(cooks)
        test_dish.ingredients.set(ingredients)
        test_dish.save()

    def test_create_dish(self):
        dish = Dish.objects.get(id=1)
        dish_type = DishType.objects.get(id=1)
        cooks = Cook.objects.all()
        ingredients = Ingredient.objects.all()

        self.assertEqual(dish.name, "test_dish")
        self.assertEqual(dish.description, "test-description")
        self.assertEqual(dish.type, dish_type)
        self.assertEqual(list(dish.cooks.all()), list(cooks))
        self.assertEqual(list(dish.ingredients.all()), list(ingredients))

    def test_dish_str(self):
        dish = Dish.objects.get(id=1)
        expected_str = f"{dish.name} (price: {dish.price}, type: {dish.type})"
        self.assertEqual(str(dish), expected_str)
