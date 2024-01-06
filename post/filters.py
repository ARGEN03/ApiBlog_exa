import django_filters
from rest_framework import filters
from .models import Post

class PostModelFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'category']

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)
