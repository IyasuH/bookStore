from django import forms
from .models import Book, Author, Order
from django.contrib.auth.models import User
from django.utils import timezone

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

class UpdateAccountForm(forms.ModelForm):
    """
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')
        exclude = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'password')
        read_ponly_fields = ('id')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_login = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if commit:
            user.save()
        return user