# Changed news to community in this file
import graphene

from graphene_django.types import DjangoObjectType

# from bootcamp.news.models import News
from bootcamp.community.models import Community
from bootcamp.helpers import paginate_data


class CommunityType(DjangoObjectType): # Changed news to community
    """DjangoObjectType to acces the Community model.""" # Changed news to community

    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        # model = News
        model = Community

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


class CommunityPaginatedType(graphene.ObjectType): # Changed news to Community
    """A paginated type generic object to provide pagination to the Community 
    graph.""" # Changed news to Community

    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    # objects = graphene.List(NewsType)
    objects = graphene.List(CommunityType)


class CommunityQuery(object): # Changed news to community
    # all_news = graphene.List(NewsType)
    all_community = graphene.List(CommunityType)
    # paginated_news = graphene.Field(NewsPaginatedType, page=graphene.Int())
    paginated_community = graphene.Field(CommunityPaginatedType, page=graphene.Int())
    # news = graphene.Field(NewsType, uuid_id=graphene.String())
    community = graphene.Field(CommunityType, uuid_id=graphene.String())

    def resolve_all_community(self, info, **kwargs):
        # return News.objects.filter(reply=False)
        return Community.objects.filter(reply=False)

    def resolve_paginated_community(self, info, page): # Change news to community
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        # qs = News.objects.filter(reply=False)
        qs = Community.objects.filter(reply=False)
        # return paginate_data(qs, page_size, page, NewsPaginatedType)
        return paginate_data(qs, page_size, page, CommunityPaginatedType)

    def resolve_community(self, info, **kwargs): # Changed news to community
        uuid_id = kwargs.get("uuid_id")
        print("uuid_id" + uuid_id)
        if uuid_id is not None:
            # return News.objects.get(uuid_id=uuid_id)
            print("uuid_id" + uuid_id)
            return Community.objects.get(uuid_id=uuid_id)

        return None


class CommunityMutation(graphene.Mutation): # Changed news to community
    """Mutation to create community objects on a efective way.""" # Changed news to community

    class Arguments:
        content = graphene.String()
        user = graphene.ID()
        parent = graphene.ID()

    content = graphene.String()
    user = graphene.ID()
    parent = graphene.ID()
    # news = graphene.Field(lambda: News)
    community = graphene.Field(lambda: Community)

    def mutate(self, **kwargs):
        print(kwargs)
