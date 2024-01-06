from rest_framework import serializers
from .models import Post
from category.models import Category
from comment.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Category.objects.all()
    )
    comments = serializers.SerializerMethodField(method_name='get_comments')
    likes = serializers.SerializerMethodField(method_name='get_likes_counter')

    def get_likes_counter(self, instance):
        likes_counter = instance.likes.all().count()
        return likes_counter

    def get_comments(self, instance):
        comments = instance.comments.all()
        serializer = CommentSerializer(
            comments, many=True
        )
        return serializer.data

    class Meta:
        fields = '__all__'
        model = Post

