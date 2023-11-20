from django.shortcuts import render
from testapp.models import Book, Author
from django.http import HttpResponse
from testapp.forms import NewBookForm

#Render() -> can be used to render templates and return a HTML page

# Create your views here.
# function that recieves requests and gives a response (request handler)

#view function must be mapped to an url (when user navigates to that url: this function will be called)

# def say_hello(request):
#     return HttpResponse('Hello World')

#This function executes when there is a request from this URL
def sayhello(request):
    context = {}
    form = NewBookForm()
    books = Book.objects.all()
    context['books'] = books
    context['title'] = 'Home'
     
    if request.method == 'POST':
        if 'save' in request.POST:
            #print(request.POST)
            form = NewBookForm(request.POST)
            form.save()
            newBook = form.save(commit=False)
            # print(newBook)
            #print(newBook)
            newBook.save()
            form.save_m2m()
        elif 'edit' in request.POST:
            primKey = request.POST.get('edit')
            book = Book.objects.get(id=primKey)
            form = NewBookForm(instance=book)

        elif 'delete' in request.POST:
            primKey = request.POST.get('delete')
            print(request.POST)
            # print(primKey)
            book = Book.objects.get(id=primKey)
            book.delete()
    elif request.method == "GET":
            print(request.GET)
            btn = request.GET.get('radio1')
            if btn == 'author':
                 print('author has been searched')
                 try:
                    trgtAuthor = Author.objects.get(name=request.GET.get('search-value')) 
                    # trgtBooks = trgtAuthor.books.all()
                    print(len(trgtBooks))
                 except Author.DoesNotExist:
                    trgtBooks = None

            elif btn == 'book':
                 print('book has been searched')  
                 print(request.GET.get('search-value'))
                 
                 try:
                    trgtBooks = Book.objects.get(title=request.GET.get('search-value')) 
                 except Book.DoesNotExist:
                    trgtBooks = None

                 context['trgtBooks'] = trgtBooks 
            else:
                 print('wrong output')
    else:
        context['trgtBooks'] = None
            

    context['form'] = form
    return render(request, 'home.html', context)




