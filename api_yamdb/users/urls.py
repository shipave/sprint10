from django.urls import include, path
from rest_framework import routers

from .views import ConfirmationView, SignupView, UserViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view()),
    path('token/', ConfirmationView.as_view())
]
