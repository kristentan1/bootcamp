# I THINK I AM GOING TO HAVE TO CHANGE THIS. COPIED AND PASTED FROM THE bootcamp/news/views.py FILE.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from bootcamp.helpers import ajax_required, AuthorRequiredMixin
# from bootcamp.news.models import News
from bootcamp.favorites.models import Favorites


class FavoritesListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""

    # model = News
    model = Favorites
    paginate_by = 15

    def get_queryset(self, **kwargs):
        # return News.objects.filter(reply=False)
        print(Favorites.objects)
        return Favorites.objects.filter(reply=False)


class FavoritesDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView): # Changed news to favorite
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""

    # model = News
    model = Favorites
    # success_url = reverse_lazy("news:list")
    success_url = reverse_lazy("favorite:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_favorite(request): # Changed news to favorite
    """A function view to implement the post functionality with AJAX allowing
    to create Favorite instances as parent ones.""" # Changed news to favorite
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print(request)
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    user = request.user
    post = '<h5>Title\n</h5>' + request.POST.getlist('post')[0] + '\n\n\n\n' + '<h5>Description\n</h5>' + request.POST.getlist('post')[1] + '\n\n' + '<h5>Link\n</h5>' + request.POST.getlist('post')[2]
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(str(request.POST.getlist('post')))
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # post = post.strip()
    if 0 < len(post) <= 1000:
        # posted = News.objects.create(user=user, content=post)
        posted = Favorites.objects.create(user=user, content = post)
        html = render_to_string(
            # "news/news_single.html", {"news": posted, "request": request}
            "favorite/favorite_single.html", {"favorite":posted, "request": request}
        )
        return HttpResponse(html)

    else:
        length = len(post) - 1000
        return HttpResponseBadRequest(
            content=_(f"Text is {length} characters longer than accepted.")
        )


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """Function view to receive AJAX, returns the count of likes a given favorite
    has recieved.""" # Changed news to favorite
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(request.POST)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    favorite_id = request.POST["favorite"] 
    print("favorite_id" + favorite_id)
    # favorite_id = request.POST.get('favorite', 'some_default')
    favorite = Favorites.objects.get(pk=favorite_id)
    user = request.user
    favorite.switch_like(user)
    return JsonResponse({"likes": favorite.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of favorite with the given favorite as parent.""" # Changed news to favorite
    # news_id = request.GET["news"]
    # news = News.objects.get(pk=news_id)
    # news_html = render_to_string("news/news_single.html", {"news": news})
    # thread_html = render_to_string(
    #     "news/news_thread.html", {"thread": news.get_thread(), "request": request}
    # )
    # return JsonResponse({"uuid": news_id, "news": news_html, "thread": thread_html})
    favorite_id = request.GET["favorite"]
    favorite = Favorites.objects.get(pk=favorite_id)
    favorite_html = render_to_string("favorite/favorite_single.html", {"favorite": favorite})
    thread_html = render_to_string(
        "favorite/favorite_thread.html", {"thread": favorite.get_thread(), "request": request}
    )
    return JsonResponse({"uuid": favorite_id, "favorite": favorite_html, "thread": thread_html})


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    Favorite instances who happens to be the children and commenters of the root
    post.""" # Changed news to favorite
    user = request.user
    post = request.POST["reply"]
    par = request.POST["parent"]
    # parent = News.objects.get(pk=par)
    parent = Favorites.objects.get(pk=par)
    post = post.strip()
    if post:
        parent.reply_this(user, post)
        return JsonResponse({"comments": parent.count_thread()})

    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST["id_value"]
    # news = News.objects.get(pk=data_point)
    favorite = Favorites.objects.get(pk=data_point)
    # data = {"likes": news.count_likers(), "comments": news.count_thread()}
    data = {"likes": favorite.count_likers(), "comments": favorite.count_thread()}
    return JsonResponse(data)
