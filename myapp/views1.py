# Import necessary classes
from django.http import HttpResponse

from .models import Publisher, Book


# Create your views here.
def index(request):
    response = HttpResponse()
    book_list = Book.objects.all().order_by('pk')
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in book_list:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    response.write('</br>')
    publisher_list = Publisher.objects.all().order_by('-city')
    heading1 = '<p>' + 'List of Publishers: ' + '</p>'
    response.write(heading1)
    for publisher in publisher_list:
        para = '<p>' + publisher.name + ', ' + publisher.city + '</p>'
        response.write(para)

    return response


def about(request):
    return HttpResponse('This is an eBook APP')


def detail(request, book_id):
    response = HttpResponse()
    book = Book.objects.get(id=book_id)
    title = '<p>Book name: ' + book.title.upper() + '</p>'
    price = '<p>Price: $' + str(book.price) + '</p>'
    publisher = '<p>Publisher: ' + book.publisher.name + '</p>'
    response.write(title)
    response.write(price)
    response.write(publisher)
    return response
