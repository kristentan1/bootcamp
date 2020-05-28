# Changed news to research in whole file
from django.conf.urls import url

# from bootcamp.news import views
from bootcamp.research import views

app_name = "research"
urlpatterns = [
    # url(r"^$", views.NewsListView.as_view(), name="list"),
    url(r"^$", views.ResearchListView.as_view(), name="list"),
    url(
        # r"^delete/(?P<pk>[-\w]+)/$", views.NewsDeleteView.as_view(), name="delete_news"
        r"^delete/(?P<pk>[-\w]+)/$", views.ResearchDeleteView.as_view(), name="delete_research"
    ),
    # url(r"^post-news/$", views.post_news, name="post_news"),
    url(r"^post-research/$", views.post_research, name="post_research"),
    url(r"^like/$", views.like, name="like_post"),
    url(r"^attended/$", views.attended, name="attended_post"),
    url(r"^get-thread/$", views.get_thread, name="get_thread"),
    url(r"^post-comment/$", views.post_comment, name="post_comments"),
    url(
        r"^update-interactions/$", views.update_interactions, name="update_interactions"
    ),
]
