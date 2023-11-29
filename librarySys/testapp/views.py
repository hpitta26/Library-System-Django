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
    books = Book.objects.all()
    context['books'] = books
    context['title'] = 'Home'
    context['trgtBooks'] = []
    context['authorRegStatus'] = request.session.get('authorRegStatus')
    context['editBookId'] = ''
     
    if (request.method == "GET") and (len(request.GET) != 0):
        request.session['editBookId'] = -1
        request.session['authorRegStatus'] = ''
        # print(request.GET)
        btn = request.GET.get('radio1') # returns value of radio1 that was clicked
        if btn == 'author':
            trgtAuthor = Author.objects.filter(name__iexact=request.GET.get('search-value'))
            # if Author with target name is found
            if len(trgtAuthor) != 0:
                trgtAuthor = Author.objects.filter(name__iexact=request.GET.get('search-value'))[0]
                trgtBooks = trgtAuthor.books.all()
                context['trgtBooks'] += trgtBooks        
        elif btn == 'book':
            # if you use (Book.objects.get() need to use try-catch since if no Book is found an exception will be thrown)
            # print(request.GET.get('search-value'))   
            trgtBook = Book.objects.filter(title__iexact=request.GET.get('search-value')) # __iexact --> case insensitive filter
            context['trgtBooks'] += trgtBook
        # else:
        #     print('wrong output')


    # Manage edited book
    context['editBookId'] = -1
    if request.session.get('editBookId') != -1 and request.session.get('editBookId') != None: #case --> Edit btn clicked
        print(request.session.get('editBookId'))
        bothEditVals = request.session.get('editBookId').split()
        oldEdit = int(bothEditVals[0])
        newEdit = int(bothEditVals[1])
        if oldEdit != newEdit: # Populate Form
            context['editBookId'] = newEdit
            editBook = Book.objects.get(pk=newEdit)
            context['form'] = NewBookForm(instance=editBook)
        else:
            context['form'] = NewBookForm()
    else:
        context['form'] = NewBookForm()

    print("Edit Book:", context['editBookId'])
        

    return render(request, 'home.html', context)







def saveFunc(request):
    if 'save' in request.POST:
        try:            
            form = NewBookForm(request.POST)
            newBook = form.save(commit=False)
            if len(Book.objects.filter(title__iexact=newBook.title)) == 0: # check to ensure case insensitivity condition is not broken
                newBook.save()
                form.save_m2m()  
        except:
            pass
    else: #save with active EDIT
        req = request.POST
        editBook = Book.objects.get(pk=int(request.session.get('editBookId').split()[1])) # entry in DB

        editBook.authors.clear() #remove all authors
        editBook.authors.add(Author.objects.get(pk=req.get('authors'))) # !!! Currently only adds 1 author !!!

        editBook.title = req.get('title')
        editBook.pages = req.get('pages')
        editBook.genre = req.get('genre')
        editBook.published_by = req.get('published_by')
        editBook.quote = req.get('quote')
        editBook.save() #save entry back to DB

    request.session['authorRegStatus'] = ''
    request.session['editBookId'] = -1

    return redirect(loadNsearchFunc) # redirects to view that is rendering the content







def deleteFunc(request):
    if 'delete' in request.POST:
        #delete the book
        targetBook = request.POST.get('delete')
        # print(targetBook)
        book = Book.objects.get(id=targetBook)
        book.delete()
        request.session['editBookId'] = -1
    else: #save target book.id
        request.session['editBookId'] = request.POST.get('edit')

    request.session['authorRegStatus'] = ''

    return redirect(loadNsearchFunc)








def regAuthorFunc(request):
    print(request.POST)
    authorName = request.POST.get('author-name').strip()
    res = ''

    if 'register' in request.POST:
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
                # UPDATE: ONLY DELETE BOOKS WITH 1 AUTHOR
                author.books.all().delete() # All of the Author's books are deleted too
                author.delete()
                res = 'Author Successfully Deleted'
            except:
                res = 'Error When Deleting Author'
        else:
            res = 'Author Not Found'


    request.session['authorRegStatus'] = res
    request.session['editBookId'] = -1

    return redirect('loadNsearchFunc')




