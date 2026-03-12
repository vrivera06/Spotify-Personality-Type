import requests
import urllib.parse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


SPOTIFY_AUTH_URL  = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE  = "https://api.spotify.com/v1"


def get_auth_url() -> str:
    """Build the Spotify OAuth authorization URL."""
    params = {
        "client_id":     settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri":  settings.SPOTIFY_REDIRECT_URI,
        "scope":         settings.SPOTIFY_SCOPES,
        "show_dialog":   "true",
    }
    return f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code(code: str) -> dict:
    """Exchange authorization code for access + refresh tokens."""
    resp = requests.post(SPOTIFY_TOKEN_URL, data={
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  settings.SPOTIFY_REDIRECT_URI,
        "client_id":     settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    })
    resp.raise_for_status()
    return resp.json()


def refresh_access_token(refresh_token: str) -> dict:
    """Use refresh token to get a new access token."""
    resp = requests.post(SPOTIFY_TOKEN_URL, data={
        "grant_type":    "refresh_token",
        "refresh_token": refresh_token,
        "client_id":     settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    })
    resp.raise_for_status()
    return resp.json()


def get_valid_token(user) -> str:
    """Return a valid access token, refreshing if expired."""
    if user.token_expires and timezone.now() >= user.token_expires:
        data = refresh_access_token(user.refresh_token)
        user.access_token = data["access_token"]
        user.token_expires = timezone.now() + timedelta(seconds=data["expires_in"])
        user.save(update_fields=["access_token", "token_expires"])
    return user.access_token


def spotify_get(endpoint: str, token: str) -> dict:
    """Make an authenticated GET request to the Spotify API."""
    resp = requests.get(
        f"{SPOTIFY_API_BASE}{endpoint}",
        headers={"Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()
    return resp.json()


def fetch_top_tracks(token: str, time_range: str = "medium_term", limit: int = 20) -> list:
    data = spotify_get(f"/me/top/tracks?time_range={time_range}&limit={limit}", token)
    return data.get("items", [])


def fetch_audio_features(track_ids: list[str], token: str) -> list:
    ids = ",".join(track_ids)
    data = spotify_get(f"/audio-features?ids={ids}", token)
    return [f for f in data.get("audio_features", []) if f]


def fetch_user_profile(token: str) -> dict:
    return spotify_get("/me", token)
