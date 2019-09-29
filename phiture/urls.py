from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from players.views import SearchView, HomeView, TeamView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view() , name='search'),
    url(r'^team/$', TeamView.as_view(), name='team'),
]
