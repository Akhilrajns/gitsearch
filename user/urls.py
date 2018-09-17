from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import GitUsersView
router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^search/$', GitUsersView.as_view(), name='web'),
]