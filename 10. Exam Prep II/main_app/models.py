from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from .helper import CreationDateMixin


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return (
            self.annotate(order_count=models.Count('order'))
            .filter(order_count__gt=2)
            .order_by('-order_count')
        )


class Profile(CreationDateMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15
    )
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()


class Product(CreationDateMixin):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    in_stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)


class Order(CreationDateMixin):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    is_completed = models.BooleanField(default=False)
