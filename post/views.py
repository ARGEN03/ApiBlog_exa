from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from comment.serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from like.models import Like



class StandartResultPagination(PageNumberPagination):
    page_size = 2
    page_query_param= 'page'

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['title', 'body']
    filterset_fields = ['category']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(method='POST', request_body=CommentSerializer, operation_description='add comment for post')
    @action(detail=True, methods=['POST'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, owner=request.user)
        return Response('успешно добавлено', 201)
    
    @action(detail=True, methods=['POST'])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        like = request.user.likes.filter(post=post)
        if like:
            like.delete()
            return Response('успешно удалено', 204)
        like = Like.objects.create(
            post=post,
            owner=request.user
        )
        return Response('успешно добавлено', 201)


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.query_params.get('search', None)
    #     # query_params = {'search':'asdf', 'category':1}
    #     if search_query:
    #         queryset = queryset.filter(title__icontains=search_query)
    #         # ILIKE %search_query%
    #     return queryset

    


# class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     lookup_field = 'id'
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
    

# написать FullCRUD на ModelViewSet(Post)
# n+1 & lazy queryset
# mixins | generics
# написать логику поиска и филтрации для постов
# написать кастомный permission который проверяет поле is_staff| staff status

# написать модельку комметариев в отделном приложении "comment"
# с полями content, owner, created_at, post
# crud & serializer & @action
# написать логику favorites
# CRD