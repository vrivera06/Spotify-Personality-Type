from django.db import models


class SpotifyUser(models.Model):
    spotify_id      = models.CharField(max_length=255, unique=True)
    display_name    = models.CharField(max_length=255, blank=True)
    email           = models.EmailField(blank=True)
    profile_image   = models.URLField(blank=True)
    access_token    = models.TextField()
    refresh_token   = models.TextField()
    token_expires   = models.DateTimeField(null=True)
    personality_type = models.CharField(max_length=100, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} ({self.spotify_id})"

    class Meta:
        db_table = 'spotify_users'


class Song(models.Model):
    spotify_track_id = models.CharField(max_length=255, unique=True)
    name             = models.CharField(max_length=500)
    artist           = models.CharField(max_length=500)
    album            = models.CharField(max_length=500, blank=True)
    album_art        = models.URLField(blank=True)
    # Spotify audio features
    energy           = models.FloatField(default=0)
    valence          = models.FloatField(default=0)
    danceability     = models.FloatField(default=0)
    acousticness     = models.FloatField(default=0)
    tempo            = models.FloatField(default=0)
    speechiness      = models.FloatField(default=0)
    instrumentalness = models.FloatField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.artist}"

    class Meta:
        db_table = 'songs'


class UserTopSong(models.Model):
    """Junction table: which songs are in a user's top tracks."""
    user      = models.ForeignKey(SpotifyUser, on_delete=models.CASCADE, related_name='top_songs')
    song      = models.ForeignKey(Song, on_delete=models.CASCADE)
    rank      = models.IntegerField()
    time_range = models.CharField(max_length=20, default='medium_term')  # short/medium/long
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_top_songs'
        unique_together = ('user', 'song', 'time_range')
