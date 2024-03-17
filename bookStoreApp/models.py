from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    # 
    class Gender(models.TextChoices):
        MALE = "M"
        FEMALE = "F"
    full_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=1,
        choices=Gender,
        default=Gender.FEMALE # stastics says most authors are women 
    )
    dob = models.DateField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='author_photo/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    # 
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Book(models.Model):
    # 
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    cover_image = models.ImageField(upload_to='book_cover/', null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    # this is by assuming people could buy multiple books at once
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=9)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    # this is the single book Item
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    # 
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
