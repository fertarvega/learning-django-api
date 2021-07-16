""" Posts ViewSet """

# Django REST framework
# from users import serializers
from rest_framework import viewsets, mixins
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from posts.permissions import IsAuthor

# Models
from posts.models import Post, Author

# Serializer
from posts.serializer import AuthorModelSerializer, PostModelSerializer

class PostsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """ Posts Model Viewset """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Save the author of the post """
        post = serializer.save()
        user = self.request.user
        Author.objects.create(author=user, post=post)

    def get_permissions(self):
        """ Assing permissions base on action """
        permissions = [IsAuthenticated]

        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor)

        return [permissions() for permissions in permissions]

    def retrieve(self, request, *args, **kwargs):
        """ Bring the data of the post with the author """

        instance = self.get_object()
        # serializer = self.get_serializer(instance)
        author = Author.objects.get(post=instance.pk)
        serializer = AuthorModelSerializer(author)
        return Response (serializer.data)

    def list(self, request, *arg, **kwargs):
        """ List all posts data with authors """

        queryset = Author.objects.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AuthorModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AuthorModelSerializer(queryset, many=True)
        return Response(serializer.data)