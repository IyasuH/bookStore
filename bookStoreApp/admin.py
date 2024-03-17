from django.contrib import admin
from .models import Author, Category, Book, Order, OrderItem, Review

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)