from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_Auth

from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Q

from .models import Book, Author, Order, Category, Review
from .forms import BookCreateForm, OrderCreateForm, UpdateAccountForm

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
        return redirect('login')
    detail = get_object_or_404(User, pk=request.user.id)
    # User.objects.get(pk=request.user.id)
    form = UpdateAccountForm(request.POST or None, instance=detail)
    if form.is_valid():
        form.save()
    return render(request, "bookStoreApp/account.html", {"form":form})    
    

# Books
class ListBooks(ListView):
    model=Book
    paginate_by=10
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

class DetailBook(DetailView):
    model=Book        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # book_id = 
        id_value = self.object.id
        # print("[INFO] book_id: ", id_value)

        # context['id'] = id_value
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

def addReview():
    """
    """
    