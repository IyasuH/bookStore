from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_Auth

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
    #Generate a transaction reference
    tx_ref = string.ascii_lowercase
    return ''.join(random.choice(tx_ref) for i in range(length))

def check_payemnt(request, tx_ref):
    """
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
    When buy button clicked
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
    model=Book
    paginate_by=10
    template_name = "bookStoreApp/book_list.html"
    def get_queryset(self):
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
        context =  super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context

class CreateBook(CreateView):
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

class DetailBook(DetailView):
    model=Book
    template_name = "bookStoreApp/book_detail.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # book_id = 
        id_value = self.object.id
        context['reviews'] = Review.objects.filter(book_id=id_value).all()
        list_review = list(context['reviews'])
        print("reviews: ", list(context['reviews']))
        tot_rating = 0
        num_rating = len(list_review)
        for review in list_review:
            tot_rating += review.rating
            print(review.rating)
        if num_rating != 0:
            context['avg_rating'] = round((tot_rating/num_rating),  2)
        context['avg_rating'] = 0
        context['review_number'] = num_rating
        return context

# Authors
class ListAuthor(ListView):
    model=Author
    paginate_by=10

class DetailAuthor(DetailView):
    model=Author

# Orders
class CreateOrder(CreateView):
    model=Order
    form_class=OrderCreateForm
    template_name='bookStoreApp/_create.html'
    success_url='/books/'

def addReview(request, book_id):
    """
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
        print(f"[INFO] rating_val, {rating_val}")
        # comment_val = request.POST.get("comment")
        form_ = ReviewCreateForm(request.POST)
        print("[INFO] ", form_)
        if form_.is_valid():
            isinstance = form_.save(commit=False)

            isinstance.book = book_
            isinstance.user = request.user
            print("[INFO] about to save data")
            form_.save()

        return redirect("book_detail", pk=book_id)
    
    return redirect("list_books")

    