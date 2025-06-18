from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Cook, Dish, DishType, Ingredient

COOK_LIST_URL = reverse("kitchen:cook-list")
COOK_CREATE_URL = reverse("kitchen:cook-create")
COOK_DETAIL_URL = reverse("kitchen:cook-detail", kwargs={"pk": 1})
COOK_UPDATE_URL = reverse("kitchen:cook-update", kwargs={"pk": 1})
COOK_DELETE_URL = reverse("kitchen:cook-delete", kwargs={"pk": 1})

DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")
DISH_TYPE_CREATE_URL = reverse("kitchen:dish-type-create")
DISH_TYPE_UPDATE_URL = reverse("kitchen:dish-type-update", kwargs={"pk": 1})
DISH_TYPE_DELETE_URL = reverse("kitchen:dish-type-delete", kwargs={"pk": 1})

INGREDIENT_LIST_URL = reverse("kitchen:ingredient-list")
INGREDIENT_CREATE_URL = reverse("kitchen:ingredient-create")
INGREDIENT_UPDATE_URL = reverse("kitchen:ingredient-update", kwargs={"pk": 1})
INGREDIENT_DELETE_URL = reverse("kitchen:ingredient-delete", kwargs={"pk": 1})

DISH_LIST_URL = reverse("kitchen:dish-list")
DISH_CREATE_URL = reverse("kitchen:dish-create")
DISH_DETAIL_URL = reverse("kitchen:dish-detail", kwargs={"pk": 1})
DISH_UPDATE_URL = reverse("kitchen:dish-update", kwargs={"pk": 1})
DISH_DELETE_URL = reverse("kitchen:dish-delete", kwargs={"pk": 1})


class PublicCookTest(TestCase):
    def test_login_required_cook_list(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cook_create(self):
        response = self.client.get(COOK_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cook_detail(self):
        response = self.client.get(COOK_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cook_update(self):
        response = self.client.get(COOK_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cook_delete(self):
        response = self.client.get(COOK_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

        Cook.objects.create(
            username="Cook_1",
            password="test1234",
            years_of_experience=2,
        )
        Cook.objects.create(
            username="Cook_2",
            password="test1234",
            years_of_experience=4,
        )

    def test_retrieve_cook_list(self):
        response = self.client.get(COOK_LIST_URL)
        cooks = Cook.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["cook_list"]), list(cooks))
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_cook_list_search(self):
        response = self.client.get(COOK_LIST_URL, {"username": "1"})
        cooks = Cook.objects.filter(username__icontains="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["cook_list"]), list(cooks))

    def test_retrieve_cook_create(self):
        response = self.client.get(COOK_CREATE_URL)
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 6,
        }
        self.client.post(COOK_CREATE_URL, form_data)
        new_user = Cook.objects.get(username=form_data["username"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(
            new_user.years_of_experience,
            form_data["years_of_experience"]
        )
        self.assertTemplateUsed(response, "kitchen/cook_form.html")

    def test_retrieve_cook_detail(self):
        response = self.client.get(COOK_DETAIL_URL)
        cook = Cook.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cook"], cook)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")

    def test_retrieve_cook_update(self):
        response = self.client.get(COOK_UPDATE_URL)
        cook = Cook.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cook"], cook)
        self.assertTemplateUsed(response, "kitchen/cook_form.html")

    def test_retrieve_cook_delete(self):
        response = self.client.get(COOK_DELETE_URL)
        cook = Cook.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cook"], cook)
        self.assertTemplateUsed(response, "kitchen/cook_confirm_delete.html")


class PublicDishTypeTest(TestCase):
    def test_login_required_dish_type_list(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_type_create(self):
        response = self.client.get(DISH_TYPE_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_type_update(self):
        response = self.client.get(DISH_TYPE_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_type_delete(self):
        response = self.client.get(DISH_TYPE_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

        DishType.objects.create(name="Dish_type_1")
        DishType.objects.create(name="Dish_type_2")

    def test_retrieve_dish_type_list(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        dish_types = DishType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types)
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_dish_type_list_search(self):
        response = self.client.get(DISH_TYPE_LIST_URL, {"name": "1"})
        dish_types = DishType.objects.filter(name__icontains="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types)
        )

    def test_retrieve_dish_type_create(self):
        response = self.client.get(DISH_TYPE_CREATE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_form.html")

    def test_retrieve_dish_type_update(self):
        response = self.client.get(DISH_TYPE_UPDATE_URL)
        dish_type = DishType.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish_type"], dish_type)
        self.assertTemplateUsed(response, "kitchen/dish_type_form.html")

    def test_retrieve_dish_type_delete(self):
        response = self.client.get(DISH_TYPE_DELETE_URL)
        dish_type = DishType.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish_type"], dish_type)
        self.assertTemplateUsed(
            response,
            "kitchen/dish_type_confirm_delete.html"
        )


class PublicIngredientTest(TestCase):
    def test_login_required_ingredient_list(self):
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_ingredient_create(self):
        response = self.client.get(INGREDIENT_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_ingredient_update(self):
        response = self.client.get(INGREDIENT_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_ingredient_delete(self):
        response = self.client.get(INGREDIENT_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)

        Ingredient.objects.create(name="Ingredient_1")
        Ingredient.objects.create(name="Ingredient_2")

    def test_retrieve_ingredient_list(self):
        response = self.client.get(INGREDIENT_LIST_URL)
        ingredients = Ingredient.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients)
        )
        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")

    def test_ingredient_list_search(self):
        response = self.client.get(INGREDIENT_LIST_URL, {"name": "1"})
        ingredients = Ingredient.objects.filter(name__icontains="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients)
        )

    def test_retrieve_ingredient_create(self):
        response = self.client.get(INGREDIENT_CREATE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/ingredient_form.html")

    def test_retrieve_ingredient_update(self):
        response = self.client.get(INGREDIENT_UPDATE_URL)
        ingredient = Ingredient.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["ingredient"], ingredient)
        self.assertTemplateUsed(response, "kitchen/ingredient_form.html")

    def test_retrieve_ingredient_delete(self):
        response = self.client.get(INGREDIENT_DELETE_URL)
        ingredient = Ingredient.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["ingredient"], ingredient)
        self.assertTemplateUsed(
            response,
            "kitchen/ingredient_confirm_delete.html"
        )


class PublicDishTest(TestCase):
    def test_login_required_dish_list(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_create(self):
        response = self.client.get(DISH_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_detail(self):
        response = self.client.get(DISH_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_update(self):
        response = self.client.get(DISH_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_dish_delete(self):
        response = self.client.get(DISH_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)

        dish_type = DishType.objects.create(name="test_dish_type_")
        Dish.objects.create(
            name="Dish_1",
            description="test_description_1",
            price=13,
            type_id=dish_type.id
        )
        Dish.objects.create(
            name="Dish_2",
            description="test_description_2",
            price=10,
            type_id=dish_type.id
        )

    def test_retrieve_dish_list(self):
        response = self.client.get(DISH_LIST_URL)
        dishes = Dish.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_dish_list_search(self):
        response = self.client.get(DISH_LIST_URL, {"name": "1"})
        dishes = Dish.objects.filter(name__icontains="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dish_list"]), list(dishes))

    def test_retrieve_dish_create(self):
        response = self.client.get(DISH_CREATE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")

    def test_retrieve_dish_detail(self):
        response = self.client.get(DISH_DETAIL_URL)
        dish = Dish.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish"], dish)
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")

    def test_retrieve_dish_update(self):
        response = self.client.get(DISH_UPDATE_URL)
        dish = Dish.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish"], dish)
        self.assertTemplateUsed(response, "kitchen/dish_form.html")

    def test_retrieve_dish_delete(self):
        response = self.client.get(DISH_DELETE_URL)
        dish = Dish.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish"], dish)
        self.assertTemplateUsed(response, "kitchen/dish_confirm_delete.html")
