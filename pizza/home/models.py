from django.db import models
from django.db.models import Sum

# The User model is a built-in model provided by Django's auth app
# that allows you to handle user authentication and authorization in your application.
from django.contrib.auth.models import User

# import uuid models
import uuid

# Create your models here.------------------------------------------------------------------

# I like to add uuid.
# Add extra Meta class to use this class as "Base Class".
# UUID stands for Universally Unique Identifier.
# UUIDs are often used instead of integer primary keys in Django models
# when you need to ensure that each record has a unique identifier,
# but you don't want to expose the sequential nature of integer primary keys or risk collision with other primary keys in a distributed system.


class BaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


# -------------------------------------------------------------------------------------------

# Pizza Category model, it inherits BaseModel features.
class PizzaCategory(BaseModel):
    category_name = models.CharField(max_length=100)


# --------------------------------------------------------------------------------------------

# Pizza model, it inherits BaseModel features.

# on_delete=models.CASCADE specifies that when a PizzaCategory instance is deleted,
# all related Pizza instances should be deleted as well.

# related_name="pizzas" specifies the name of the reverse relation from PizzaCategory to Pizza,
# which can be used to access all Pizza instances related to a particular PizzaCategory instance.
# This will return a queryset containing all Pizza instances related to the category instance.
class Pizza(BaseModel):
    category = models.ForeignKey(
        PizzaCategory, on_delete=models.CASCADE, related_name="pizzas")
    pizza_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.ImageField(upload_to='pizza')


# ----------------------------------------------------------------------------------------------

# Cart model, it inherits BaseModel features.

# on_delete=models.SET_NULL , if any user delets then also we can see their cart details.
class Cart(BaseModel):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="carts")
    is_paid = models.BooleanField(default=False)
    instamojo_id = models.CharField(max_length=1000)

    def get_cart_total(self):
        return CartItems.objects.filter(cart=self).aggregate(Sum('pizza__price'))['pizza__price__sum']


# ----------------------------------------------------------------------------------------------

# Cart Items model
class CartItems(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
