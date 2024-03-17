from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    path('authors/', views.ListAuthor.as_view(), name='list_authors'),
    path('author/<int:pk>/', views.DetailAuthor.as_view(), name='author_deatil'),
    path('books/', views.ListBooks.as_view(), name="list_books"),
    path('book/<int:pk>/', views.DetailBook.as_view(), name="book_detail"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]