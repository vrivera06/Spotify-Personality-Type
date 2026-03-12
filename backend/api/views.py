import json
from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .analysis import generate_personality
from .models import Song, SpotifyUser, UserTopSong
from .spotify import (
    exchange_code,
    fetch_audio_features,
    fetch_top_tracks,
    fetch_user_profile,
    get_auth_url,
    get_valid_token,
)


# ── Auth ────────────────────────────────────────────────────────────────────

@require_GET
def login(request):
    """Redirect the user to Spotify's OAuth consent screen."""
    return redirect(get_auth_url())


@require_GET
def callback(request):
    """
    Spotify redirects here after user grants permission.
    Exchange code → tokens, upsert user, redirect to React frontend.
    """
    error = request.GET.get("error")
    if error:
        return redirect(f"http://localhost:3000?error={error}")

    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Missing code"}, status=400)

    try:
        token_data = exchange_code(code)
    except Exception as e:
        return redirect(f"http://localhost:3000?error=token_exchange_failed")

    access_token  = token_data["access_token"]
    refresh_token = token_data.get("refresh_token", "")
    expires_in    = token_data.get("expires_in", 3600)

    try:
        profile = fetch_user_profile(access_token)
    except Exception:
        return redirect("http://localhost:3000?error=profile_fetch_failed")

    user, _ = SpotifyUser.objects.update_or_create(
        spotify_id=profile["id"],
        defaults={
            "display_name":  profile.get("display_name", ""),
            "email":         profile.get("email", ""),
            "profile_image": (profile.get("images") or [{}])[0].get("url", ""),
            "access_token":  access_token,
            "refresh_token": refresh_token or "",
            "token_expires": timezone.now() + timedelta(seconds=expires_in),
        },
    )
    if not refresh_token and user.refresh_token:
        pass  # keep existing refresh token

    return redirect(f"http://localhost:3000/dashboard?user_id={user.spotify_id}")


# ── User ────────────────────────────────────────────────────────────────────

@require_GET
def user_profile(request, spotify_id):
    try:
        user = SpotifyUser.objects.get(spotify_id=spotify_id)
    except SpotifyUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({
        "spotify_id":     user.spotify_id,
        "display_name":   user.display_name,
        "email":          user.email,
        "profile_image":  user.profile_image,
        "personality_type": user.personality_type,
    })


# ── Analysis ─────────────────────────────────────────────────────────────────

@require_GET
def analyze(request, spotify_id):
    """
    Full pipeline:
      1. Fetch top tracks from Spotify
      2. Fetch audio features for those tracks
      3. Persist songs + user–song links to DB
      4. Run personality analysis
      5. Return result
    """
    try:
        user = SpotifyUser.objects.get(spotify_id=spotify_id)
    except SpotifyUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    time_range = request.GET.get("time_range", "medium_term")

    try:
        token  = get_valid_token(user)
        tracks = fetch_top_tracks(token, time_range=time_range, limit=20)
    except Exception as e:
        return JsonResponse({"error": f"Spotify fetch failed: {str(e)}"}, status=502)

    if not tracks:
        return JsonResponse({"error": "No top tracks found"}, status=404)

    track_ids = [t["id"] for t in tracks]

    try:
        features = fetch_audio_features(track_ids, token)
    except Exception as e:
        return JsonResponse({"error": f"Audio feature fetch failed: {str(e)}"}, status=502)

    # ── Persist songs ──────────────────────────────────────────────────────
    feature_map = {f["id"]: f for f in features if f and "id" in f}

    for rank, track in enumerate(tracks, start=1):
        tid = track["id"]
        feat = feature_map.get(tid, {})
        song, _ = Song.objects.update_or_create(
            spotify_track_id=tid,
            defaults={
                "name":             track["name"],
                "artist":           ", ".join(a["name"] for a in track.get("artists", [])),
                "album":            track.get("album", {}).get("name", ""),
                "album_art":        (track.get("album", {}).get("images") or [{}])[0].get("url", ""),
                "energy":           feat.get("energy", 0),
                "valence":          feat.get("valence", 0),
                "danceability":     feat.get("danceability", 0),
                "acousticness":     feat.get("acousticness", 0),
                "tempo":            feat.get("tempo", 0),
                "speechiness":      feat.get("speechiness", 0),
                "instrumentalness": feat.get("instrumentalness", 0),
            },
        )
        UserTopSong.objects.update_or_create(
            user=user, song=song, time_range=time_range,
            defaults={"rank": rank},
        )

    # ── Personality ────────────────────────────────────────────────────────
    result = generate_personality(features)

    user.personality_type = result["type"]
    user.save(update_fields=["personality_type"])

    top_tracks_payload = [
        {
            "name":      t["name"],
            "artist":    ", ".join(a["name"] for a in t.get("artists", [])),
            "album_art": (t.get("album", {}).get("images") or [{}])[0].get("url", ""),
        }
        for t in tracks[:10]
    ]

    return JsonResponse({
        "personality": result,
        "top_tracks":  top_tracks_payload,
        "user": {
            "display_name":  user.display_name,
            "profile_image": user.profile_image,
        },
    })


# ── Top tracks (cached from DB) ───────────────────────────────────────────

@require_GET
def top_tracks(request, spotify_id):
    try:
        user = SpotifyUser.objects.get(spotify_id=spotify_id)
    except SpotifyUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    time_range = request.GET.get("time_range", "medium_term")
    uts = (
        UserTopSong.objects
        .filter(user=user, time_range=time_range)
        .select_related("song")
        .order_by("rank")[:20]
    )

    tracks = [
        {
            "rank":      ut.rank,
            "name":      ut.song.name,
            "artist":    ut.song.artist,
            "album_art": ut.song.album_art,
            "energy":    ut.song.energy,
            "valence":   ut.song.valence,
        }
        for ut in uts
    ]
    return JsonResponse({"tracks": tracks})
