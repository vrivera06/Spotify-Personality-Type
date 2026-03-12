# Spotify Personality Type

> Analyze your Spotify listening data and discover your music personality archetype.

Built with **Django** · **React** · **MySQL** · **Spotify OAuth 2.0** — Fall 2024

---

## Overview

Spotify Personality Type is a full-stack web application that connects to your Spotify account via secure OAuth 2.0, pulls your top tracks and listening history through the Spotify Web API, and runs an analysis pipeline to generate a personality archetype based on your unique audio profile.

Released and actively used by 10+ real listeners.

---

## Features

- **Listening Analysis** — Fetches top tracks and audio features (energy, valence, danceability, acousticness, tempo) from the Spotify Web API
- **Personality Insights** — Maps audio feature averages to 16 distinct archetypes (e.g. The Midnight Wanderer, The Euphoric Optimist, The Quiet Architect)
- **Secure OAuth 2.0** — Full Spotify authorization code flow with token refresh; zero passwords stored
- **Persistent Storage** — MySQL-backed models for users, songs, and user–song relationships with time-range tracking
- **Time Range Support** — Analyze your last 4 weeks, 6 months, or all-time listening

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Django 4.2 + Django REST Framework |
| Frontend   | React 18 + React Router |
| Database   | MySQL (SQLite for local dev) |
| Auth       | Spotify OAuth 2.0 (Authorization Code Flow) |
| Data       | Spotify Web API         |

---

## Architecture

```
Spotify API (OAuth 2.0)
       ↓
Django REST Backend  ←→  MySQL Database
       ↓
  React Frontend
```

**Auth flow:**
1. User clicks "Connect with Spotify"
2. Django redirects to Spotify's OAuth consent screen
3. Spotify redirects back to `/api/callback/` with an authorization code
4. Django exchanges the code for access + refresh tokens
5. User profile is upserted into MySQL
6. React frontend receives `user_id` and calls `/api/analyze/{user_id}/`

---

## Project Structure

```
spotify-personality/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── spotify_personality/
│   │   ├── settings.py        # Django config, DB, CORS, Spotify credentials
│   │   └── urls.py
│   └── api/
│       ├── models.py          # SpotifyUser, Song, UserTopSong
│       ├── views.py           # OAuth callback, analyze, top-tracks endpoints
│       ├── spotify.py         # Spotify API helpers + token refresh
│       ├── analysis.py        # Personality engine
│       └── urls.py
└── frontend/
    ├── package.json
    └── src/
        ├── App.js             # Router
        ├── index.css          # Global design system
        └── pages/
            ├── Landing.js     # Hero, features, connect CTA
            ├── Landing.module.css
            ├── Dashboard.js   # Personality result + top tracks
            └── Dashboard.module.css
```

---

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL (optional — SQLite used by default for local dev)
- A [Spotify Developer App](https://developer.spotify.com/dashboard) with a registered redirect URI

---

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/spotify-personality-type
cd spotify-personality-type
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/callback/
DJANGO_SECRET_KEY=your-secret-key

# Optional — leave blank to use SQLite
# DB_NAME=spotify_personality
# DB_USER=root
# DB_PASSWORD=yourpassword
```

> In your Spotify Developer Dashboard, add `http://localhost:8000/api/callback/` as a Redirect URI.

### 4. Run migrations and start the backend

```bash
python manage.py migrate
python manage.py runserver
```

Backend runs at `http://localhost:8000`

### 5. Set up the frontend

```bash
cd ../frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000`

---

## API Endpoints

| Method | Endpoint                          | Description                              |
|--------|-----------------------------------|------------------------------------------|
| GET    | `/api/login/`                     | Redirect to Spotify OAuth                |
| GET    | `/api/callback/`                  | Handle OAuth callback, create/update user |
| GET    | `/api/user/{spotify_id}/`         | Get user profile + personality type     |
| GET    | `/api/analyze/{spotify_id}/`      | Run full analysis, persist songs, return result |
| GET    | `/api/top-tracks/{spotify_id}/`   | Return cached top tracks from DB        |

**Query params for `/analyze/` and `/top-tracks/`:**
- `time_range` — `short_term` (4 weeks) · `medium_term` (6 months) · `long_term` (all time)

### Example response from `/api/analyze/{id}/`

```json
{
  "personality": {
    "type": "The Midnight Wanderer",
    "emoji": "🌙",
    "desc": "Introspective, emotionally rich, and drawn to complex soundscapes.",
    "scores": {
      "energy": 28,
      "valence": 32,
      "danceability": 41,
      "acousticness": 72
    }
  },
  "top_tracks": [
    { "name": "Track Name", "artist": "Artist", "album_art": "https://..." }
  ],
  "user": {
    "display_name": "Alex",
    "profile_image": "https://..."
  }
}
```

---

## Database Models

```python
SpotifyUser     # spotify_id, display_name, tokens, personality_type
Song            # track metadata + audio features (energy, valence, danceability…)
UserTopSong     # user ↔ song junction with rank + time_range
```

---

## Personality Types

| Archetype              | Emoji | Signature Traits              |
|------------------------|-------|-------------------------------|
| The Midnight Wanderer  | 🌙    | Low energy, low valence       |
| The Euphoric Optimist  | ⚡    | High energy, high valence, danceable |
| The Quiet Architect    | 🌿    | High acousticness, lower energy |
| The Fearless Rebel     | 🔥    | Very high energy, lower valence |
| The Dream Chaser       | ✨    | Mid energy, positive valence  |
| The Nostalgic Soul     | 🎞️    | Acoustic, mid valence         |
| The Kinetic Spirit     | 🎯    | Very high danceability        |
| The Deep Thinker       | 🧠    | Balanced / default            |

---

## Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.
