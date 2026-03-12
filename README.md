# 🎵 Spotify Personality Type

A full-stack web app that connects to your Spotify account, analyzes your listening history, and generates a personality profile based on your music taste. Currently used by 10+ active users.

![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify_API-1DB954?style=flat&logo=spotify&logoColor=white)

---

## 🧰 Technologies Used

- **Frontend:** React
- **Backend:** Django
- **Database:** MySQL
- **Auth:** OAuth 2.0 via Spotify
- **API:** Spotify Web API

---

## ✨ Features

- Secure Spotify login via OAuth 2.0
- Pulls and analyzes your top tracks, artists, and genres
- Generates a unique personality type based on listening patterns
- Stores user and song data for returning users
- Clean, responsive UI

---

## ⚙️ Process

I started this project wanting to combine two things I enjoy — music and data. The biggest challenge was working with Spotify's OAuth flow and making sure tokens were handled securely on the backend. I used Django to manage all API calls and MySQL to store user and song data. On the frontend, I built the UI in React, focusing on making the personality results feel personal and fun.

**What I learned:**
- How OAuth 2.0 authentication works end to end
- Managing third-party API rate limits and token refresh cycles
- Structuring a full-stack Django + React project from scratch

---

## 🚀 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/vrivera06/spotify-personality-type.git

# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend setup (in a new terminal)
cd frontend
npm install
npm start
```

> You'll need a Spotify Developer account. Add your `CLIENT_ID` and `CLIENT_SECRET` to a `.env` file before running.

---

## 🔮 How It Could Be Improved

- Compare personality types with friends
- Generate playlists based on your personality result
- Expand insight categories with more listening data points
