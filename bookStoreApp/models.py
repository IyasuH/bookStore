from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from djmoney.models.fields import MoneyField

class Author(models.Model):
    # id - auto increment generated id
    class Gender(models.TextChoices):
        MALE = "M"
        FEMALE = "F"
    full_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=1,
        choices=Gender,
        default=Gender.FEMALE # stastics says most authors are women :|
    )
    dob = models.DateField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='author_photo/', null=True, blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    # id - auto increment generated id
    name = models.CharField(max_length=40)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    # id - auto increment generated id
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="ETB")
    # price = models.DecimalField(decimal_places=2, max_digits=6)
    cover_image = models.ImageField(upload_to='book_cover/', null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # fields for next migartion
    # publised_at = models.DateTimeField(null=True)


    def __str__(self):
        return self.title

class Order(models.Model):
    # id - auto increment generated id
    # data from this model is created after the call back of stripe webhook
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, default=1, null=True)
    # shipping_info - that will be returned from stripe
    email = models.EmailField(null=True)
    full_name = models.CharField(null=True)
    country = models.CharField(max_length=50, default="Ethiopia")
    address_line_1 = models.CharField(null=True)
    address_line_2 = models.CharField(null=True)
    postal_code = models.CharField(null=True)
    city = models.CharField(default="Addis Ababa", null=True)
    phone_number = models.CharField(null=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    # id - auto increment generated id
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # order id
    stripe_transaction_id = models.CharField(max_length=300) # stripe transaction id
    status = models.CharField(max_length=50) # pending, succeede, failed
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency="ETB")
    # amount = models.DecimalField(decimal_places=2, max_digits=7) # 100
    currency = models.CharField(max_length=10, default="ETB") # ETB
    # why currency conversion rate -- conevrsion from what currency ?? - what was i thinking - 
    # i think i just copied the return values from stripe 
    currency_conversion_rate = models.DecimalField(decimal_places=4, max_digits=12) # conversion rate to ETB
    payment_method = models.CharField(max_length=100) # debit card, credit card, other walets,...
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    # id - auto increment generated id
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    rating = models.PositiveIntegerField()
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
