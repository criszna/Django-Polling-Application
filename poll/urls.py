from django.conf.urls import url
from . import views

app_name = 'poll'
urlpatterns = [
    url('create/', views.create, name='create'),
    url('vote/(?P<poll_id>\d+)/', views.vote, name='vote'),
    url('results/(?P<poll_id>\d+)/', views.results, name='results'),
    url('edit/(?P<poll_id>\d+)/', views.edit, name='edit'),
    url('delete/(?P<poll_id>\d+)/', views.delete, name='delete'),
    url('', views.home, name='home'),
]