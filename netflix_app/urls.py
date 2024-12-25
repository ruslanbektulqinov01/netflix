from django.urls import path, include

from .views import MovieViewSet, ActorViewSet, MovieActorAPIView, CommentAPIView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()


router.register("movies", MovieViewSet)
router.register("actors", ActorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("movies/<int:pk>/actors/", MovieActorAPIView.as_view(), name="movie-actors"),
    path("comments/", CommentAPIView.as_view(), name="comments"),
    path("comments/<int:pk>/", CommentAPIView.as_view(), name="comments"),
    path("auth/", obtain_auth_token, name="auth-token"),
]
