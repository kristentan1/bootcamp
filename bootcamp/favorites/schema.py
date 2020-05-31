# Changed news to favorite in this file
import graphene

from graphene_django.types import DjangoObjectType

# from bootcamp.news.models import News
from bootcamp.favorites.models import Favorites
from bootcamp.news.models import News
from bootcamp.news.schema import NewsType
from bootcamp.research.schema import ResearchType
from bootcamp.research.models import Research
from bootcamp.helpers import paginate_data


class FavoritesType(DjangoObjectType): # Changed news to favorite
    """DjangoObjectType to acces the Favorite model.""" # Changed news to favorite

    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        # model = News
        model = Favorites

    def resolve_count_thread(self, info, **kwargs):
        return self.get_thread().count()

    def resolve_count_likers(self, info, **kwargs):
        return self.get_likers().count()

    def resolve_get_thread(self, info, **kwargs):
        return self.get_thread()

    def resolve_get_likers(self, info, **kwargs):
        return self.get_likers()


class FavoritePaginatedType(graphene.ObjectType): # Changed news to favorite
    """A paginated type generic object to provide pagination to the favorite 
    graph.""" # Changed news to favorite

    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    # objects = graphene.List(NewsType)
    objects = graphene.List(NewsType)
    researchobjects = graphene.List(ResearchType)


class FavoriteQuery(object): # Changed news to favorite
    # all_news = graphene.List(NewsType)
    all_favorite = graphene.List(NewsType)
    # paginated_news = graphene.Field(NewsPaginatedType, page=graphene.Int())
    paginated_favorite = graphene.Field(FavoritePaginatedType, page=graphene.Int())
    # news = graphene.Field(NewsType, uuid_id=graphene.String())
    favorite = graphene.Field(FavoritesType, uuid_id=graphene.String())

    def resolve_all_favorite(self, info, **kwargs):
        # return News.objects.filter(reply=False)
        return Favorites.newsobjects.filter(reply=False)

    def resolve_paginated_favorite(self, info, page): # Change news to favorite
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        # qs = News.objects.filter(reply=False)
        qs = Favorites.newsobjects.filter(reply=False)
        # return paginate_data(qs, page_size, page, NewsPaginatedType)
        return paginate_data(qs, page_size, page, FavoritePaginatedType)

    def resolve_favorite(self, info, **kwargs): # Changed news to favorite
        uuid_id = kwargs.get("uuid_id")
        print("uuid_id" + uuid_id)
        if uuid_id is not None:
            # return News.objects.get(uuid_id=uuid_id)
            print("uuid_id" + uuid_id)
            return Favorites.newsobjects.get(uuid_id=uuid_id)

        return None


class FavoriteMutation(graphene.Mutation): # Changed news to favorite
    """Mutation to create favorite objects on a efective way.""" # Changed news to favorite

    class Arguments:
        content = graphene.String()
        user = graphene.ID()
        parent = graphene.ID()

    content = graphene.String()
    user = graphene.ID()
    parent = graphene.ID()
    # news = graphene.Field(lambda: News)
    favorite = graphene.Field(lambda: Favorites)

    def mutate(self, **kwargs):
        print(kwargs)
