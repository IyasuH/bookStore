from django import forms
from .models import Book, Author, Order

class BookCreateForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Book
        # fields = ('id', 'title', 'description', 'price', 'cover_image', 'created_at', 'updated_at', 'author_id')
        exclude = ('id', 'created_at', 'updated_at')

class OrderCreateForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Order
        # fields = ('id', 'created_at', 'updated_at', 'user_id', 'book_id', 'price')
        exclude = ('id', 'created_at', 'updated_at')
        read_only_fields = ('price')
