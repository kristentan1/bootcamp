# Changed news to internship in whole file
from django.conf.urls import url

# from bootcamp.news import views
from bootcamp.internship import views

app_name = "internship"
urlpatterns = [
    # url(r"^$", views.NewsListView.as_view(), name="list"),
    url(r"^$", views.InternshipListView.as_view(), name="list"),
    url(
        # r"^delete/(?P<pk>[-\w]+)/$", views.NewsDeleteView.as_view(), name="delete_news"
        r"^delete/(?P<pk>[-\w]+)/$", views.InternshipDeleteView.as_view(), name="delete_internship"
    ),
    # url(r"^post-news/$", views.post_news, name="post_news"),
    url(r"^post-internship/$", views.post_internship, name="post_internship"),
    url(r"^like/$", views.like, name="like_post"),
    url(r"^attended/$", views.attended, name="attended_post"),
    url(r"^get-thread/$", views.get_thread, name="get_thread"),
    url(r"^post-comment/$", views.post_comment, name="post_comments"),
    url(
        r"^update-interactions/$", views.update_interactions, name="update_interactions"
    ),
]
