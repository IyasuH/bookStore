from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_Auth
from django.core.paginator import Paginator

from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Q

from chapa import Chapa

from .models import Book, Author, Order, Category, Review, Payment
from .forms import BookCreateForm, OrderCreateForm, UpdateAccountForm, AuthorCreateForm, ReviewCreateForm

import string
import random
import os
import time
import requests

URL = "https://bookstore-0jgj.onrender.com/"

CHAPA_SECRET = os.getenv("chapa_secret_key")

class SignUp(CreateView):
    """create new user"""
    model=User
    form_class=UserCreationForm
    template_name='bookStoreApp/signup.html'
    success_url='/login/'

def login(request):
    """
    users login
    """
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login_auth(request, auth_user)
            return redirect('list_books')
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

def account(request):
    """
    user account to see their data including 
    - user info
    - purchase history
    - reviews
    - carts
    """
    if not request.user.is_authenticated:
        messages.info(request, "First login")
        return redirect('login')
    detail = get_object_or_404(User, pk=request.user.id)
    # User.objects.get(pk=request.user.id)
    form = UpdateAccountForm(request.POST or None, instance=detail)
    if form.is_valid():
        form.save()
    return render(request, "bookStoreApp/account.html", {"form":form})    

def generete_tx_ref(length):
    """Generate a transaction reference for chapa"""
    tx_ref = string.ascii_lowercase
    return ''.join(random.choice(tx_ref) for i in range(length))

def check_payemnt(request, tx_ref):
    """
    to check the payment using transaction reference for chapa
    - then to create data on payment table
    """
    url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    payload = ''
    headers = {
        'Authorization': f"Bearer {CHAPA_SECRET}"
    }
    
    response = requests.get(url, headers=headers, data=payload)
    response_ = response.json()

    if response_["status"] == 'success':
        # create payment data
        print("[INFO - PAY] successful payment")

    return HttpResponse()


def buy_book(request, book_id):
    """
    When buy button clicked, will redirects to chapa payment page(test currently)
    """
    if not request.user.is_authenticated:
        # user not authenticated redirect to login page
        messages.info(request, "First you have to login")
        return redirect('login')
    # create order
    order_ = Order()

    # firts check if user is loggedin
    user_ = get_object_or_404(User, id=request.user.id)
    book_ = get_object_or_404(Book, id=book_id)
    # time.sleep(.5)

    # check all required user data is filled in db
    if user_.first_name == "" or user_.last_name == "" or user_.email == "":
        # not full enough info redirect to account page
        messages.info(request, "Not Enough Info")
        return redirect('account')

    tx_ref_ = generete_tx_ref(12)

    data = {
        'email': user_.email,
        'first_name': user_.first_name,
        'last_name': user_.last_name,
        'amount': book_.price.amount,
        'currency': book_.price.currency,
        'tx_ref': tx_ref_,
        'callback_url': f"{URL}/verify_payment/{tx_ref_}",

		'customization': {
			'title': "bookStore",
            # i am only displayiong limmited info on the desc because, chapa kind of have some str limitaion
			'description': f"payment for book id {book_.id}",
		}
    }

    chapa = Chapa(CHAPA_SECRET)
    response = chapa.initialize(**data)

    if response['status'] == 'success':
        print("[INFO] order successful, save on db")

        order_ = Order()
        order_.user = user_
        order_.book = book_
        order_.email = user_.email
        order_.full_name = f"{user_.first_name} {user_.last_name}"

        order_.save()
    else:
        print("[INFO] payment faled")

    print ("[INFO] response: ", response)
    return redirect(response['data']['checkout_url'])    

# Books
class ListBooks(ListView):
    """
    list books with 10 objects per page 
    """
    
    model=Book
    paginate_by=10
    template_name = "bookStoreApp/book_list.html"
    def get_queryset(self):
        """
        to handle the search and category query
        """
        
        search_query = self.request.GET.get('search')
        category_query = self.request.GET.get('category')
        queryvalue = super().get_queryset()
        if search_query:
            # because of the following error i am unable to search based on category, Author
            # Unsupported lookup 'contains' for ForeignKey or join on the field not permitted 
            queryvalue = Book.objects.filter(Q(description__contains=search_query) | Q(title__contains=search_query))
        elif category_query:
            queryvalue = Book.objects.filter(categories__name__icontains=category_query)
        return queryvalue

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """to list categories"""
        context =  super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context

class CreateBook(CreateView):
    """To create book using the defined form[BookCreateForm]"""
    model=Book
    form_class=BookCreateForm
    template_name='bookStoreApp/_create.html'
    success_url='/books/'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "you have to login first")
            return redirect("login")
        elif not request.user.is_staff:
            messages.info(request, "you don't have access to do that")
            return redirect("login")
        return super().get(request, *args, **kwargs)        

class CreateAuthor(CreateView):
    """to create author using the defined form[AuthorCreateForm]"""
    model=Author
    form_class=AuthorCreateForm
    template_name='bookStoreApp/_create.html'
    success_url ='/authors/'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "you have to login first")
            return redirect("login")
        elif not request.user.is_staff:
            messages.info(request, "you don't have access to do that")
            return redirect("login")
        return super().get(request, *args, **kwargs)        


class DetailBook(DetailView):
    model=Book
    template_name = "bookStoreApp/book_detail.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        to list reviews for specifc book
        """
        context = super().get_context_data(**kwargs)
        # book_id = 
        id_value = self.object.id
        reviews = Review.objects.filter(book_id=id_value).all()

        paginator = Paginator(reviews, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['reviews'] = page_obj
        context['avg_rating'] = self.calculate_avg_rating(list(context['reviews']))
        context['review_number'] = reviews.count()

        return context
    
    def calculate_avg_rating(self, reviews):
        """
        calculates average rating
        """
        tot_rating = sum(review.rating for review in reviews)
        num_ratings = len(reviews)
        if num_ratings != 0:
            return round(tot_rating/num_ratings, 2)
        else:
            return 0

# Authors
class ListAuthor(ListView):
    model=Author
    paginate_by=10
    template_name="bookStoreApp/author_list.html"

class DetailAuthor(DetailView):
    model=Author
    template_name="bookStoreApp/author_detail.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        to list books writen by the author
        """
        context = super().get_context_data(**kwargs)
        id_value = self.object.id        
        books = Book.objects.filter(author=id_value).all()

        context['books'] = books


# Orders
# i don't think this will be needed
# class CreateOrder(CreateView):
#     model=Order
#     form_class=OrderCreateForm
#     template_name='bookStoreApp/_create.html'
#     success_url='/books/'

def addReview(request, book_id):
    """
    handles add review
    """
    if request.method == "POST":
        """
        creating review for a book
        """
        if not request.user.is_authenticated:
            # user not authenticated redirect to login page
            messages.info(request, "First you have to login")
            return redirect('login')

        print(f"[INFO] book_id: {book_id}, \n user: {request.user}")

        book_ = get_object_or_404(Book, id=book_id)

        rating_val = request.POST.get("rating")
        # comment_val = request.POST.get("comment")
        form_ = ReviewCreateForm(request.POST)
        if form_.is_valid():
            isinstance = form_.save(commit=False)

            isinstance.book = book_
            isinstance.user = request.user
            print("[INFO] about to save data")
            form_.save()

        return redirect("book_detail", pk=book_id)

    return redirect("list_books")
