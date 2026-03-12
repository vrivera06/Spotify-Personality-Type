from django.urls import path
from . import views

urlpatterns = [
    path('login/',                          views.login,        name='login'),
    path('callback/',                       views.callback,     name='callback'),
    path('user/<str:spotify_id>/',          views.user_profile, name='user-profile'),
    path('analyze/<str:spotify_id>/',       views.analyze,      name='analyze'),
    path('top-tracks/<str:spotify_id>/',    views.top_tracks,   name='top-tracks'),
]
