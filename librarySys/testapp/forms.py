from django import forms
from testapp.models import Book, Author

class NewBookForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all()) 
    # authors = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    pages = forms.IntegerField()
    genre = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    published_by = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    quote = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))

    class Meta:
        model = Book
        exclude = ()
        # fields = ['title', 'authors', 'pages', 'genre', 'published_by', 'quote']
        # widgets = {
        #     "title": forms.Textarea(attrs={"cols": 0, "rows": 0}),
        #     "authors": forms.Textarea(attrs={"cols": 0, "rows": 0}),
        #     "pages": forms.Textarea(attrs={"cols": 0, "rows": 0}),
        #     "genre": forms.Textarea(attrs={"cols": 0, "rows": 0}),
        #     "published_by": forms.Textarea(attrs={"cols": 0, "rows": 0}),
        #     "quote": forms.Textarea(attrs={"cols": 0, "rows": 0})
        # }


class SearchForm(forms.Form):
    searchValue = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))