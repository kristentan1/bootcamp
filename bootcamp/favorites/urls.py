# Changed news to favorite in whole file
from django.conf.urls import url

# from bootcamp.news import views
from bootcamp.favorites import views

app_name = "favorite"
urlpatterns = [
    # url(r"^$", views.NewsListView.as_view(), name="list"),
    url(r"^$", views.FavoritesListView.as_view(), name="list"),
    url(
        # r"^delete/(?P<pk>[-\w]+)/$", views.NewsDeleteView.as_view(), name="delete_news"
        r"^delete/(?P<pk>[-\w]+)/$", views.FavoritesDeleteView.as_view(), name="delete_favorite"
    ),
    # url(r"^post-news/$", views.post_news, name="post_news"),
    url(r"^post-favorites/$", views.post_favorite, name="post_favorite"),
    url(r"^like/$", views.like, name="like_post"),
    url(r"^get-thread/$", views.get_thread, name="get_thread"),
    url(r"^post-comment/$", views.post_comment, name="post_comments"),
    url(
        r"^update-interactions/$", views.update_interactions, name="update_interactions"
    ),
]
