# Changed news to favorite in whole file
from django.conf.urls import url

# from bootcamp.news import views
from bootcamp.favorites import views

app_name = "favorite"
urlpatterns = [
    # url(r"^$", views.NewsListView.as_view(), name="list"),
    url(r"^$", views.FavoritesListView.as_view(), name="list"),
    
]
