# Changed news to research in this file
import graphene

from graphene_django.types import DjangoObjectType

# from bootcamp.news.models import News
from bootcamp.research.models import Research
from bootcamp.helpers import paginate_data


class ResearchType(DjangoObjectType): # Changed news to research
    """DjangoObjectType to acces the Research model.""" # Changed news to research

    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        # model = News
        model = Research

    def resolve_count_thread(self, info, **kwargs):
        return self.get_thread().count()

    def resolve_count_likers(self, info, **kwargs):
        return self.get_likers().count()
    
    def resolve_count_attendees(self, info, **kwargs):
        return self.get_attendees().count()

    def resolve_get_thread(self, info, **kwargs):
        return self.get_thread()

    def resolve_get_likers(self, info, **kwargs):
        return self.get_likers()
    
    def resolve_get_attendees(self, info, **kwargs):
        return self.get_attendees()


class ResearchPaginatedType(graphene.ObjectType): # Changed news to research
    """A paginated type generic object to provide pagination to the research 
    graph.""" # Changed news to research

    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    # objects = graphene.List(NewsType)
    objects = graphene.List(ResearchType)


class ResearchQuery(object): # Changed news to research
    # all_news = graphene.List(NewsType)
    all_research = graphene.List(ResearchType)
    # paginated_news = graphene.Field(NewsPaginatedType, page=graphene.Int())
    paginated_research = graphene.Field(ResearchPaginatedType, page=graphene.Int())
    # news = graphene.Field(NewsType, uuid_id=graphene.String())
    research = graphene.Field(ResearchType, uuid_id=graphene.String())

    def resolve_all_research(self, info, **kwargs):
        # return News.objects.filter(reply=False)
        return Research.objects.filter(reply=False)

    def resolve_paginated_research(self, info, page): # Change news to research
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        # qs = News.objects.filter(reply=False)
        qs = Research.objects.filter(reply=False)
        # return paginate_data(qs, page_size, page, NewsPaginatedType)
        return paginate_data(qs, page_size, page, ResearchPaginatedType)

    def resolve_research(self, info, **kwargs): # Changed news to research
        uuid_id = kwargs.get("uuid_id")
        print("uuid_id" + uuid_id)
        if uuid_id is not None:
            # return News.objects.get(uuid_id=uuid_id)
            print("uuid_id" + uuid_id)
            return Research.objects.get(uuid_id=uuid_id)

        return None


class ResearchMutation(graphene.Mutation): # Changed news to research
    """Mutation to create research objects on a efective way.""" # Changed news to research

    class Arguments:
        content = graphene.String()
        user = graphene.ID()
        parent = graphene.ID()

    content = graphene.String()
    user = graphene.ID()
    parent = graphene.ID()
    # news = graphene.Field(lambda: News)
    research = graphene.Field(lambda: Research)

    def mutate(self, **kwargs):
        print(kwargs)
