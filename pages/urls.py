# pages/urls.py
from django.urls import path
from .views import homePageView, results, homePost

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path('<int:genHlth>/<int:age>/<int:diffWalking>/<int:highBP>/<int:stroke>/<int:highChol>/results/',
         results, name='results'),
]

