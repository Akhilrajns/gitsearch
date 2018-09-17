from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import GitUsersView, AdminReports
router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^search/$', GitUsersView.as_view(), name='user-search'),
    url(r'^reports/$', AdminReports.as_view(), name='reports'),
]