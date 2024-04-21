from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from bookStoreApp.models import Book, Category, Author, Order, Review

from bookStoreAPI.serializers import BookSerializer, CategorySerializer, AuthorSerializer, OrderSerializer, ReviewSerializer

from django.contrib.auth.models import User

from bookStoreAPI.permissions import ReadOnlyPermission, IsReviewOwner
# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    """
    Book API
        - GET books/ - to get all books
        - GET books/{id} - to get one book
        - POST books/ - to create book
        - PUT books/{id} - to update book data
        - DELETE books/{id} - to delete book data
    """
    queryset = Book.objects.all().order_by('created_at')
    serializer_class = BookSerializer
    permission_classes = [ReadOnlyPermission]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category API
        - GET category/ - to get all categories
        - GET category/{id} - to get one category
        - POST category/ - to create category
        - PUT category/{id} - to update category data
        - DELETE category/{id} - to delete category data
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyPermission]

class AuthorViewSet(viewsets.ModelViewSet):
    """
    Author API
        - GET author/ - to get all authors
        - GET author/{id} - to get one author
        - POST author/ - to create author
        - PUT author/{id} - to update author data
        - DELETE author/{id} - to delete author data
    """
    queryset = Author.objects.all().order_by('created_at')
    serializer_class = AuthorSerializer
    permission_classes = [ReadOnlyPermission]

# Order Model has to be changed 
class OrderViewSet(viewsets.ModelViewSet):
    """
    Order API
        - GET order/ - to get all orders
        - GET order/{id} - to get one order
        - POST order/ - to create order
        - PUT order/{id} - to update order data
        - DELETE order/{id} - to delete order data
    """
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Review API
        - GET review/ - to get all reviews
        - GET review/{id} - to get one review
        - POST review/ - to create review
        - PUT review/{id} - to update review data
        - DELETE review/{id} - to delete review data   
    """
    queryset = Review.objects.all().order_by('created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

