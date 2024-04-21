from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    # authors CRUD
    path('app/authors/', views.ListAuthor.as_view(), name='list_authors'),
    path('app/author/<int:pk>/', views.DetailAuthor.as_view(), name='author_deatil'),
    # books CRUD
    path('app/books/', views.ListBooks.as_view(), name="list_books"),
    path('app/book/<int:pk>/', views.DetailBook.as_view(), name="book_detail"),
    path('app/new_book/', views.CreateBook.as_view(), name="new_book"),
    # signup, login, logout
    path('app/signup/', views.SignUp.as_view(), name="signup"),
    path('app/login/', views.login, name='login'),
    path('app/logout/', views.logout, name='logout'),
    # orders
    path('app/new_order/', views.CreateOrder.as_view(), name="new_order")
]