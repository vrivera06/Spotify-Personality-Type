from django.contrib import admin
from .models import SpotifyUser, Song, UserTopSong

@admin.register(SpotifyUser)
class SpotifyUserAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'spotify_id', 'personality_type', 'created_at']
    search_fields = ['display_name', 'spotify_id', 'email']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'energy', 'valence', 'danceability']
    search_fields = ['name', 'artist']

@admin.register(UserTopSong)
class UserTopSongAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'rank', 'time_range']
