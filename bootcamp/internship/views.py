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
from bootcamp.internship.models import Internship


class InternshipListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""

    # model = News
    model = Internship
    paginate_by = 15

    def get_queryset(self, **kwargs):
        # return News.objects.filter(reply=False)
        return Internship.objects.filter(reply=False)


class InternshipDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView): # Changed news to internship
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""

    # model = News
    model = Internship
    # success_url = reverse_lazy("news:list")
    success_url = reverse_lazy("internship:list")


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_internship(request): # Changed news to internship
    """A function view to implement the post functionality with AJAX allowing
    to create Internship instances as parent ones.""" # Changed news to internship
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print(request)
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    user = request.user
    post = '<h5>Title\n</h5>' + request.POST.getlist('post')[0] + '\n\n\n\n' + '<h5>Target Group\n</h5>' + request.POST.getlist('post')[1] + '<h5>Description\n</h5>' + request.POST.getlist('post')[2] + '\n\n' + '<h5>Duration\n</h5>' + request.POST.getlist('post')[3] + '<h5>Link\n</h5>' + request.POST.getlist('post')[4]
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(str(request.POST.getlist('post')))
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # post = post.strip()
    if 0 < len(post) <= 1000:
        # posted = News.objects.create(user=user, content=post)
        posted = Internship.objects.create(user=user, content = post)
        html = render_to_string(
            # "news/news_single.html", {"news": posted, "request": request}
            "internship/internship_single.html", {"internship":posted, "request": request}
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
    """Function view to receive AJAX, returns the count of likes a given internship
    has recieved.""" # Changed news to internship
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(request.POST)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    internship_id = request.POST["internship"] 
    print("internship_id" + internship_id)
    # internship_id = request.POST.get('internship', 'some_default')
    internship = Internship.objects.get(pk=internship_id)
    user = request.user
    internship.switch_like(user)
    return JsonResponse({"likes": internship.count_likers()})

@login_required
@ajax_required
@require_http_methods(["POST"])
def attended(request):
    """Function view to receive AJAX, returns the count of attended a given news
    has recieved."""
    internship_id = request.POST["internship"]
    internship = Internship.objects.get(pk=internship_id)
    user = request.user
    internship.switch_attend(user)
    return JsonResponse({"attendeds": internship.count_attendees()})

@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of internship with the given internship as parent.""" # Changed news to internship
    # news_id = request.GET["news"]
    # news = News.objects.get(pk=news_id)
    # news_html = render_to_string("news/news_single.html", {"news": news})
    # thread_html = render_to_string(
    #     "news/news_thread.html", {"thread": news.get_thread(), "request": request}
    # )
    # return JsonResponse({"uuid": news_id, "news": news_html, "thread": thread_html})
    internship_id = request.GET["internship"]
    internship = Internship.objects.get(pk=internship_id)
    internship_html = render_to_string("internship/internship_single.html", {"internship": internship})
    thread_html = render_to_string(
        "internship/internship_thread.html", {"thread": internship.get_thread(), "request": request}
    )
    return JsonResponse({"uuid": internship_id, "internship": internship_html, "thread": thread_html})


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    Internship instances who happens to be the children and commenters of the root
    post.""" # Changed news to internship
    user = request.user
    post = request.POST["reply"]
    par = request.POST["parent"]
    # parent = News.objects.get(pk=par)
    parent = Internship.objects.get(pk=par)
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
    internship = Internship.objects.get(pk=data_point)
    # data = {"likes": news.count_likers(), "comments": news.count_thread()}
    data = {"likes": internship.count_likers(), "comments": internship.count_thread(), "attendeds": internship.count_attendees()}
    return JsonResponse(data)
