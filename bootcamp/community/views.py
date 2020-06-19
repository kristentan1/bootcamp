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
from bootcamp.community.models import Community


class CommunityListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""

    # model = News
    model = Community
    paginate_by = 15

    def get_queryset(self, **kwargs):
        # return News.objects.filter(reply=False)
        return Community.objects.filter(reply=False)


class CommunityDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView): # Changed news to community
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""

    # model = News
    model = Community
    # success_url = reverse_lazy("news:list")
    success_url = reverse_lazy("community:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_community(request): # Changed news to community
    """A function view to implement the post functionality with AJAX allowing
    to create Community instances as parent ones.""" # Changed news to community
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print(request)
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    user = request.user
    post = '<h5>Title\n</h5>' + request.POST.getlist('post')[0] + '\n\n\n\n' + '<h5>Title\n</h5>' + request.POST.getlist('post')[1] + '<h5>Description\n</h5>' + request.POST.getlist('post')[2] + '\n\n' + '<h5>Link\n</h5>' + request.POST.getlist('post')[3]
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(str(request.POST.getlist('post')))
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # post = post.strip()
    if 0 < len(post) <= 1000:
        # posted = News.objects.create(user=user, content=post)
        posted = Community.objects.create(user=user, content = post)
        html = render_to_string(
            # "news/news_single.html", {"news": posted, "request": request}
            "community/community_single.html", {"community":posted, "request": request}
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
    """Function view to receive AJAX, returns the count of likes a given community
    has recieved.""" # Changed news to community
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(request.POST)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    community_id = request.POST["community"] 
    print("community_id" + community_id)
    # community_id = request.POST.get('community', 'some_default')
    community = Community.objects.get(pk=community_id)
    user = request.user
    community.switch_like(user)
    return JsonResponse({"likes": community.count_likers()})

@login_required
@ajax_required
@require_http_methods(["POST"])
def attended(request):
    """Function view to receive AJAX, returns the count of attended a given news
    has recieved."""
    community_id = request.POST["community"]
    community = Community.objects.get(pk=community_id)
    user = request.user
    community.switch_attend(user)
    return JsonResponse({"attendeds": community.count_attendees()})

@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of community with the given community as parent.""" # Changed news to community
    # news_id = request.GET["news"]
    # news = News.objects.get(pk=news_id)
    # news_html = render_to_string("news/news_single.html", {"news": news})
    # thread_html = render_to_string(
    #     "news/news_thread.html", {"thread": news.get_thread(), "request": request}
    # )
    # return JsonResponse({"uuid": news_id, "news": news_html, "thread": thread_html})
    community_id = request.GET["community"]
    community = Community.objects.get(pk=community_id)
    community_html = render_to_string("community/community_single.html", {"community": community})
    thread_html = render_to_string(
        "community/community_thread.html", {"thread": community.get_thread(), "request": request}
    )
    return JsonResponse({"uuid": community_id, "community": community_html, "thread": thread_html})


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    Community instances who happens to be the children and commenters of the root
    post.""" # Changed news to community
    user = request.user
    post = request.POST["reply"]
    par = request.POST["parent"]
    # parent = News.objects.get(pk=par)
    parent = Community.objects.get(pk=par)
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
    community = Community.objects.get(pk=data_point)
    # data = {"likes": news.count_likers(), "comments": news.count_thread()}
    data = {"likes": community.count_likers(), "comments": community.count_thread(), "attendeds": community.count_attendees()}
    return JsonResponse(data)
