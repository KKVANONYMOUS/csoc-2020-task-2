from django.urls import path
from authentication.views import *

urlpatterns = [
    path('', registerView, name="registerView"),
    
]