from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Publisher, Book, Member, Order, Review
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import random
from datetime import datetime


# Create your views here.
def index(request):
    last_login = ''
    if 'last_login' in request.session.keys():
        last_login = request.session.get('last_login')
    book_list = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': book_list, 'last_login': last_login})


def about(request):
    if request.COOKIES.get('lucky_num'):
        mynum = request.COOKIES.get('lucky_num')
    else:
        mynum = random.randint(1, 100)
    response = render(request, 'myapp/about.html', {'mynum': mynum})
    response.set_cookie('lucky_num', mynum, expires=300)
    return response


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/detail.html', {'book': book})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            # booklist = Book.objects.filter(category=category)
            if not category:
                booklist = Book.objects.filter(price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price, category=category)
            return render(request, 'myapp/results.html', {'booklist': booklist, 'name': name, 'category': category})
        else:
            print(form.errors)
            return render(request, 'myapp/findbooks.html', {'form': form, })
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save()
            member = order.member
            type = order.order_type
            order.save()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            book = review.book
            book.num_reviews += 1
            book.save()
            review.save()
            return HttpResponseRedirect('/myapp')
    else:
        form = ReviewForm()
    return render(request, 'myapp/review.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


def chk_reviews(request, book_id):
    # Not logged-in
    if request.user.is_anonymous:
        return HttpResponseRedirect('/myapp/login')
    if request.user.is_authenticated:
        selected_book = get_object_or_404(Book, pk=book_id)
        if selected_book.num_reviews == 0:
            return render(request, 'myapp/chk_reviews.html', {'book': selected_book, 'avg_rating': -1})
        else:
            reviews = Review.objects.filter(book=selected_book)
            total_rating = 0
            for single_review in reviews:
                total_rating += single_review.rating
            avg_rating = total_rating / len(reviews)
            return render(request, 'myapp/chk_reviews.html', {'book': selected_book, 'avg_rating': avg_rating})
    else:
        return render(request, 'myapp/chk_reviews.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/myapp')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
