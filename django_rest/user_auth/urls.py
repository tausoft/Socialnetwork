from django.conf.urls import *
from .views import LoginAPIView, RegisterAPIView, UserAPIView

app_name = 'user_auth'
urlpatterns = [
    url(r'^users/?$', UserAPIView.as_view({'get': 'list'})),
    url(r'^users/register/?$', RegisterAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
]