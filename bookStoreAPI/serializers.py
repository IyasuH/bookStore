from bookStoreApp.models import Book, Category, Author, Order, Review, Payment
from rest_framework import serializers

# class UserSerializer(serializers.)

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'cover_image', 'categories']
        read_only_fields = ['id']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields =['name', 'id']
        read_only_fields = ['id']

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields =['id', 'full_name', 'gender', 'dob', 'bio', 'photo']
        read_only_fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # user fileds not working with HyperlinkedModelSerializer
        fields =['id', 'book', 'user', 'email', 'full_name', 'country', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'phone_number']
        read_only_fields = ['user', 'id']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_transaction_id', 'status', 'amount', 'currency_conversion_rate', 'currency', 'payment_method']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id', 'book', 'comment', 'rating', 'user']
        read_only_fields = ['user', 'id']