# Changed news to internship in this file
import graphene

from graphene_django.types import DjangoObjectType

# from bootcamp.news.models import News
from bootcamp.internship.models import Internship
from bootcamp.helpers import paginate_data


class InternshipType(DjangoObjectType): # Changed news to internship
    """DjangoObjectType to acces the Internship model.""" # Changed news to internship

    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        # model = News
        model = Internship

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


class InternshipPaginatedType(graphene.ObjectType): # Changed news to Internship
    """A paginated type generic object to provide pagination to the Internship 
    graph.""" # Changed news to Internship

    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    # objects = graphene.List(NewsType)
    objects = graphene.List(InternshipType)


class InternshipQuery(object): # Changed news to internship
    # all_news = graphene.List(NewsType)
    all_internship = graphene.List(InternshipType)
    # paginated_news = graphene.Field(NewsPaginatedType, page=graphene.Int())
    paginated_internship = graphene.Field(InternshipPaginatedType, page=graphene.Int())
    # news = graphene.Field(NewsType, uuid_id=graphene.String())
    internship = graphene.Field(InternshipType, uuid_id=graphene.String())

    def resolve_all_internship(self, info, **kwargs):
        # return News.objects.filter(reply=False)
        return Internship.objects.filter(reply=False)

    def resolve_paginated_internship(self, info, page): # Change news to internship
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        # qs = News.objects.filter(reply=False)
        qs = Internship.objects.filter(reply=False)
        # return paginate_data(qs, page_size, page, NewsPaginatedType)
        return paginate_data(qs, page_size, page, InternshipPaginatedType)

    def resolve_internship(self, info, **kwargs): # Changed news to internship
        uuid_id = kwargs.get("uuid_id")
        print("uuid_id" + uuid_id)
        if uuid_id is not None:
            # return News.objects.get(uuid_id=uuid_id)
            print("uuid_id" + uuid_id)
            return Internship.objects.get(uuid_id=uuid_id)

        return None


class InternshipMutation(graphene.Mutation): # Changed news to internship
    """Mutation to create internship objects on a efective way.""" # Changed news to internship

    class Arguments:
        content = graphene.String()
        user = graphene.ID()
        parent = graphene.ID()

    content = graphene.String()
    user = graphene.ID()
    parent = graphene.ID()
    # news = graphene.Field(lambda: News)
    internship = graphene.Field(lambda: Internship)

    def mutate(self, **kwargs):
        print(kwargs)
