from django.http import HttpResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Movie, Actor, Comment
from .serializers import ActorSerializer, MovieSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title"]
    ordering_fields = ["imdb", "-imdb"]
    filterset_fields = ["genre"]
    # def get_queryset(self):
    #     queryset = Movie.objects.all()
    #     query = self.request.query_params.get('search')
    #     if query is not None:
    #         queryset = queryset.filter(title__icontains=query)
    #     return queryset

    @action(detail=True, methods=["post"])
    def add_actor(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)
        actor_id = request.data.get("actor_id")
        actor = Actor.objects.get(pk=actor_id)
        movie.actors.add(actor)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def remove_actor(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)
        actor_id = request.data.get("actor_id")
        actor = Actor.objects.get(pk=actor_id)
        movie.actors.remove(actor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieActorAPIView(APIView):
    def get(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = ActorSerializer(movie.actors.all(), many=True)
        return Response(serializer.data)


class CommentAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = CommentSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        serializer = CommentSerializer(user.comments.all(), many=True)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
