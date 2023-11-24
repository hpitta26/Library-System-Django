from django.shortcuts import render, redirect
from django.urls import reverse
from testapp.models import Book, Author
from django.http import HttpResponse
from testapp.forms import NewBookForm

#Render() -> can be used to render templates and return a HTML page

# Create your views here.
# function that recieves requests and gives a response (request handler)

#view function must be mapped to an url (when user navigates to that url: this function will be called)


#This function executes when there is a request from this URL
def loadNsearchFunc(request):
    context = {}
    form = NewBookForm()
    books = Book.objects.all()
    context['books'] = books
    context['title'] = 'Home'
    context['trgtBooks'] = []
    context['authorRegStatus'] = request.session.get('authorRegStatus')

    print(request.session.get('authorRegStatus'))

    # print('Status:' + hash)
     
    if request.method == "GET": 
        request.session['authorRegStatus'] = ''
        # print(request.GET)
        btn = request.GET.get('radio1') # returns value of radio1 that was clicked
        if btn == 'author':
            # print('author has been searched')
            trgtAuthor = Author.objects.filter(name__iexact=request.GET.get('search-value'))
            # if Author with target name is found
            if len(trgtAuthor) != 0:
                trgtAuthor = Author.objects.filter(name__iexact=request.GET.get('search-value'))[0]
                trgtBooks = trgtAuthor.books.all()
                context['trgtBooks'] += trgtBooks        
        elif btn == 'book':
            # if you use (Book.objects.get() need to use try-catch since if no Book is found an exception will be thrown)
            #print('book has been searched')  
            # print(request.GET.get('search-value'))   
            trgtBook = Book.objects.filter(title__iexact=request.GET.get('search-value')) # __iexact --> case insensitive filter
            # print(trgtBook)
            context['trgtBooks'] += trgtBook
        # else:
        #     print('wrong output')
            
    context['form'] = form
    return render(request, 'home.html', context)



def saveFunc(request):
    try:
        form = NewBookForm(request.POST)
        # form.save()
        newBook = form.save(commit=False)
        # print(newBook)
        if len(Book.objects.filter(title__iexact=newBook.title)) == 0: # check to ensure case insensitivity condition is not broken
            newBook.save()
            form.save_m2m()  
    except:
        # print('unexpected input')
        print('')

    request.session['authorRegStatus'] = ''

    return redirect(loadNsearchFunc) # redirects to view that is rendering the content



def editFunct(request):
    primKey = request.POST.get('edit')
    book = Book.objects.get(id=primKey)
    form = NewBookForm(instance=book)

    request.session['authorRegStatus'] = ''



def deleteFunc(request):
    targetBook = request.POST.get('delete')
    print(request.POST)
    # print(targetBook)
    book = Book.objects.get(id=targetBook)
    book.delete()

    request.session['authorRegStatus'] = ''

    return redirect(loadNsearchFunc)


def regAuthorFunc(request):
    print(request.POST)
    authorName = request.POST.get('author-name').strip()
    res = ''

    if 'register' in request.POST:
        # print('Register Btn Clicked')
        if len(Author.objects.filter(name__iexact=authorName)) != 0:
            #author with target name exists
            res = 'Author Already Registered'
        else:
            try:
                #try to register
                newAuthor = Author(name=authorName.title())
                newAuthor.save()
                res = 'Author Successfully Registered'
            except:
                res = 'Error When Registering Author'
    elif 'delete' in request.POST: #Implement CASCADE on delete
        print('Delete Btn Clicked')
        if len(Author.objects.filter(name__iexact=authorName)) != 0:
            try:
                #author with target name exists
                author = Author.objects.get(name=authorName.title())
                author.books.all().delete() # All of the Author's books are deleted too
                author.delete()
                res = 'Author Successfully Deleted'
            except:
                res = 'Error When Deleting Author'
        else:
            res = 'Author Not Found'


    request.session['authorRegStatus'] = res

    return redirect('loadNsearchFunc')




