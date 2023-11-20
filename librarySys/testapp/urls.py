#file where urls will be mapped to View functions
from django.urls import path
from . import views

# URLConfiguration module (every app in your project needs this)
# This needs to be imported into the main URLConfig of the project
urlpatterns = [
    path('', views.sayhello, name="sayhello")
]

