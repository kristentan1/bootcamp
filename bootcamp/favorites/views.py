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
from bootcamp.research.models import Research



class FavoritesListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""
    context_object_name = "list"
    # model = News
    #model = Favorites
    paginate_by = 15
    template_name = "favorites/favorites_list.html"
    queryset = [Research.objects.all(), Internship.objects.all()]
    
    """def get_queryset(self, **kwargs):
        # return News.objects.filter(reply=False)
        #print(Favorites.objects)
        return Research.objects.filter(reply=False)"""
        

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['research'] = Research.objects.filter(reply=False).filter(liked=self.request.user)
        context['internship'] = Internship.objects.filter(reply=False).filter(liked=self.request.user)
        print(context)
        return context



