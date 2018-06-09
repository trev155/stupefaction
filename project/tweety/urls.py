from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tweet_search/<query>/<int:num_results>', views.tweet_search, name='tweet_search')
]
