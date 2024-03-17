from typing import Any
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_Auth

from django.views.generic import ListView, CreateView, DetailView

from .models import Book, Author

class SignUp(CreateView):
    model=User
    form_class=UserCreationForm
    template_name='bookStoreApp/signup.html'
    success_url='/login/'

def login(request):
    """
    users login
    """
    if request.user.is_authenticated:
        return redirect('list_authors')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login_auth(request, auth_user)
            return redirect('list_authors')
        else:
            messages.error(request, "Wrong username or password")
    return render(request, "bookStoreApp/login.html")
    # only required to buy something

def logout(request):
    """
    users logout
    """
    logout_Auth(request)
    return redirect("list_books")

class ListBooks(ListView):
    model=Book
    paginate_by=10

class DetailBook(DetailView):
    model=Book

class ListAuthor(ListView):
    model=Author
    paginate_by=10

class DetailAuthor(DetailView):
    model=Author


def addReview():
    """
    """
    