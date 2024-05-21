from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    # authors CRUD
    path('authors/', views.ListAuthor.as_view(), name='list_authors'),
    path('author/<int:pk>/', views.DetailAuthor.as_view(), name='author_deatil'),
    path('new_author/', views.CreateAuthor.as_view(), name='new_author'),
    # books CRUD
    path('', views.ListBooks.as_view(), name="list_books"),
    path('book/<int:pk>/', views.DetailBook.as_view(), name="book_detail"),
    path('new_book/', views.CreateBook.as_view(), name="new_book"),
    # signup, login, logout
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my_account/', views.account, name='account'),
    # orders
    # path('new_order/', views.CreateOrder.as_view(), name="new_order"),
    # buy_book
    path('buy_book/<int:book_id>/', views.buy_book, name="buy_book"),
    # payment_verify
    path('verify_payment/<str:tx_ref>/', views.check_payemnt, name="check_payemnt"),
    # review
    path('write_review/<int:book_id>/', views.addReview, name="write_review"),
]