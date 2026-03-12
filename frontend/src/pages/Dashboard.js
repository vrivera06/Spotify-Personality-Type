import { useEffect, useState, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import styles from './Dashboard.module.css';

const TIME_RANGES = [
  { value: 'short_term',  label: 'Last 4 Weeks' },
  { value: 'medium_term', label: 'Last 6 Months' },
  { value: 'long_term',   label: 'All Time' },
];

function Bar({ label, value, delay = 0 }) {
  const fillRef = useRef(null);
  useEffect(() => {
    const t = setTimeout(() => {
      if (fillRef.current) fillRef.current.style.width = value + '%';
    }, delay);
    return () => clearTimeout(t);
  }, [value, delay]);

  return (
    <div className={styles.barRow}>
      <span className={styles.barLabel}>{label}</span>
      <div className={styles.barTrack}>
        <div ref={fillRef} className={styles.barFill} style={{ width: '0%' }} />
      </div>
      <span className={styles.barVal}>{value}%</span>
    </div>
  );
}

export default function Dashboard() {
  const [params]   = useSearchParams();
  const navigate   = useNavigate();
  const userId     = params.get('user_id');

  const [loading,   setLoading]   = useState(true);
  const [error,     setError]     = useState(null);
  const [data,      setData]      = useState(null);
  const [timeRange, setTimeRange] = useState('medium_term');
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    if (!userId) { navigate('/'); return; }
    runAnalysis();
    // eslint-disable-next-line
  }, [userId]);

  const runAnalysis = async (range = timeRange) => {
    setAnalyzing(true);
    setError(null);
    try {
      const res = await fetch(`/api/analyze/${userId}/?time_range=${range}`);
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Analysis failed');
      }
      const json = await res.json();
      setData(json);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
      setAnalyzing(false);
    }
  };

  const handleRangeChange = (range) => {
    setTimeRange(range);
    runAnalysis(range);
  };

  if (loading) return (
    <div className={styles.center}>
      <div className={styles.spinner} />
      <p className={styles.loadingText}>Analyzing your Spotify data…</p>
    </div>
  );

  if (error) return (
    <div className={styles.center}>
      <div className={styles.errorBox}>
        <div className={styles.errorIcon}>⚠️</div>
        <h2 style={{ fontFamily: 'Syne', fontWeight: 700, marginBottom: 8 }}>Something went wrong</h2>
        <p style={{ color: 'var(--muted)', marginBottom: 20 }}>{error}</p>
        <button className={styles.btnPrimary} onClick={() => navigate('/')}>Back to Home</button>
      </div>
    </div>
  );

  const { personality, top_tracks, user } = data;

  return (
    <div className={styles.page}>
      <div className={styles.container}>

        {/* ── Nav ── */}
        <nav className={styles.nav}>
          <div className={styles.navLogo}>
            <span style={{ color: 'var(--green)' }}>Spotify</span> Personality
          </div>
          <div className={styles.navUser}>
            {user.profile_image && (
              <img src={user.profile_image} alt="" className={styles.avatar} />
            )}
            <span className={styles.navName}>{user.display_name}</span>
          </div>
        </nav>

        {/* ── Personality Result ── */}
        <section className={styles.resultSection}>
          <div className={styles.badge}>
            <span className={styles.blink} /> Your Personality Type
          </div>

          <div className={styles.resultCard}>
            <div className={styles.resultEmoji}>{personality.emoji}</div>
            <h1 className={styles.resultType}>{personality.type}</h1>
            <p className={styles.resultDesc}>{personality.desc}</p>

            <div className={styles.bars}>
              <Bar label="Energy"       value={personality.scores.energy}       delay={200} />
              <Bar label="Valence"      value={personality.scores.valence}      delay={320} />
              <Bar label="Danceability" value={personality.scores.danceability} delay={440} />
              <Bar label="Acousticness" value={personality.scores.acousticness} delay={560} />
            </div>
          </div>
        </section>

        {/* ── Time Range ── */}
        <section>
          <div className={styles.sectionLabel}>Time Range</div>
          <div className={styles.rangeRow}>
            {TIME_RANGES.map(r => (
              <button
                key={r.value}
                className={timeRange === r.value ? styles.rangeActive : styles.rangeBtn}
                onClick={() => handleRangeChange(r.value)}
                disabled={analyzing}
              >
                {r.label}
              </button>
            ))}
            {analyzing && <span className={styles.analyzingText}>Analyzing…</span>}
          </div>
        </section>

        {/* ── Top Tracks ── */}
        <section>
          <div className={styles.sectionLabel}>Your Top Tracks</div>
          <h2 className={styles.h2}>What's been in your rotation</h2>
          <div className={styles.trackList}>
            {top_tracks.map((track, i) => (
              <div key={i} className={styles.trackRow}>
                <span className={styles.trackRank}>{String(i + 1).padStart(2, '0')}</span>
                {track.album_art && (
                  <img src={track.album_art} alt="" className={styles.trackArt} />
                )}
                <div className={styles.trackInfo}>
                  <div className={styles.trackName}>{track.name}</div>
                  <div className={styles.trackArtist}>{track.artist}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── Re-analyze ── */}
        <section className={styles.reanalyzeSection}>
          <button
            className={styles.btnPrimary}
            onClick={() => runAnalysis(timeRange)}
            disabled={analyzing}
          >
            {analyzing ? '⟳ Analyzing…' : '⟳ Re-analyze'}
          </button>
          <button
            className={styles.btnGhost}
            onClick={() => navigate('/')}
          >
            ← Back to Home
          </button>
        </section>

        <footer className={styles.footer}>
          <p>Built with ♥ · Django · React · MySQL · Spotify Web API</p>
        </footer>
      </div>
    </div>
  );
}
