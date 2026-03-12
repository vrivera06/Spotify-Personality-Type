from statistics import mean


PERSONALITIES = [
    {
        "type": "The Midnight Wanderer",
        "emoji": "🌙",
        "desc": "Introspective, emotionally rich, and drawn to complex soundscapes. You listen with intent and feel everything deeply.",
        "condition": lambda e, v, d, a: e < 0.4 and v < 0.4,
    },
    {
        "type": "The Euphoric Optimist",
        "emoji": "⚡",
        "desc": "High-energy, upbeat, and always ready to move. Your playlist is basically a perpetual celebration.",
        "condition": lambda e, v, d, a: e > 0.7 and v > 0.65 and d > 0.65,
    },
    {
        "type": "The Quiet Architect",
        "emoji": "🌿",
        "desc": "Thoughtful and deliberate — you build sonic worlds out of acoustic textures, space, and restraint.",
        "condition": lambda e, v, d, a: a > 0.6 and e < 0.5,
    },
    {
        "type": "The Fearless Rebel",
        "emoji": "🔥",
        "desc": "Loud, bold, and unapologetic. You don't just hear music — you feel it rattling in your chest.",
        "condition": lambda e, v, d, a: e > 0.75 and v < 0.5,
    },
    {
        "type": "The Dream Chaser",
        "emoji": "✨",
        "desc": "Ethereal and exploratory — you gravitate toward cinematic, expansive music that feels like a new horizon.",
        "condition": lambda e, v, d, a: 0.4 <= e <= 0.7 and v > 0.55,
    },
    {
        "type": "The Nostalgic Soul",
        "emoji": "🎞️",
        "desc": "Sentimental and story-driven. Every song is a time capsule. You listen to remember.",
        "condition": lambda e, v, d, a: a > 0.5 and v > 0.4 and e < 0.55,
    },
    {
        "type": "The Kinetic Spirit",
        "emoji": "🎯",
        "desc": "Rhythm is your language. You sync your heartbeat to the beat and lose yourself completely.",
        "condition": lambda e, v, d, a: d > 0.75,
    },
    {
        "type": "The Deep Thinker",
        "emoji": "🧠",
        "desc": "Analytical and genre-fluid. You treat music as a lens for understanding the world.",
        "condition": lambda e, v, d, a: True,  # fallback
    },
]


def generate_personality(audio_features: list[dict]) -> dict:
    """
    Analyze a list of Spotify audio feature objects and return
    a personality archetype with trait scores.
    """
    if not audio_features:
        return {
            "type": "The Deep Thinker",
            "emoji": "🧠",
            "desc": "Analytical and genre-fluid. You treat music as a lens for understanding the world.",
            "scores": {"energy": 50, "valence": 50, "danceability": 50, "acousticness": 50},
        }

    avg_energy       = mean([f.get("energy", 0)       for f in audio_features])
    avg_valence      = mean([f.get("valence", 0)       for f in audio_features])
    avg_danceability = mean([f.get("danceability", 0)  for f in audio_features])
    avg_acousticness = mean([f.get("acousticness", 0)  for f in audio_features])

    matched = next(
        (p for p in PERSONALITIES if p["condition"](avg_energy, avg_valence, avg_danceability, avg_acousticness)),
        PERSONALITIES[-1],
    )

    return {
        "type":        matched["type"],
        "emoji":       matched["emoji"],
        "desc":        matched["desc"],
        "scores": {
            "energy":       round(avg_energy * 100),
            "valence":      round(avg_valence * 100),
            "danceability": round(avg_danceability * 100),
            "acousticness": round(avg_acousticness * 100),
        },
    }
