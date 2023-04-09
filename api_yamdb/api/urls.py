from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    CommentViewSet, ReviewViewSet, ConfirmationView,
                    SignupView, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='Category')
router_v1.register('genres', GenreViewSet, basename='genre')
# router_v1.register('reviews', ReviewViewSet)
# router_v1.register(
#     r'reviews/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')

router_v1.register(r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', ConfirmationView.as_view())
]
