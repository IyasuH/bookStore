from django.contrib import admin
from .models import Author, Category, Book, Order, Review

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Review)