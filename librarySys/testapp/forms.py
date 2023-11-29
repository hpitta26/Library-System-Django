from django import forms
from testapp.models import Book, Author

class NewBookForm(forms.ModelForm):

    title = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all()) 
    pages = forms.IntegerField()
    genre = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    published_by = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))
    quote = forms.CharField(widget=forms.Textarea(attrs={"cols": 0, "rows": 0}))

    class Meta:
        model = Book
        exclude = ()