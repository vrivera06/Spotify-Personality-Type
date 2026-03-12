import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import styles from './Landing.module.css';

const FEATURES = [
  { icon: '🎵', title: 'Listening Analysis',   desc: 'Pulls your top tracks and audio features — energy, valence, tempo — from the Spotify Web API to build your full musical DNA.' },
  { icon: '🧠', title: 'Personality Insights',  desc: 'Maps audio features to 16 distinct personality archetypes, from The Midnight Wanderer to The Euphoric Optimist.' },
  { icon: '🔐', title: 'Secure OAuth 2.0',      desc: 'Industry-standard Spotify OAuth with token refresh. Zero passwords stored — auth is fully delegated to Spotify.' },
  { icon: '💾', title: 'Persistent Storage',    desc: 'MySQL-backed storage for user profiles and song data, enabling your personality history to be tracked over time.' },
];

const STACK = [
  { icon: '🐍', name: 'Django',      role: 'REST API · Auth',  bg: 'rgba(9,148,64,0.15)' },
  { icon: '⚛️', name: 'React',       role: 'Frontend UI',      bg: 'rgba(97,218,251,0.15)' },
  { icon: '🗄️', name: 'MySQL',       role: 'Database',         bg: 'rgba(0,117,143,0.15)' },
  { icon: '🎵', name: 'Spotify API', role: 'Data Source',      bg: 'rgba(29,185,84,0.15)' },
  { icon: '🔐', name: 'OAuth 2.0',   role: 'Authentication',   bg: 'rgba(255,107,107,0.15)' },
  { icon: '📦', name: 'DRF',         role: 'API Framework',    bg: 'rgba(189,147,249,0.15)' },
];

export default function Landing() {
  const [params] = useSearchParams();
  const error = params.get('error');

  useEffect(() => {
    // stagger-in sections
    const sections = document.querySelectorAll('[data-fade]');
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
        }
      });
    }, { threshold: 0.1 });
    sections.forEach(s => {
      s.style.opacity = '0';
      s.style.transform = 'translateY(20px)';
      s.style.transition = 'opacity 0.55s ease, transform 0.55s ease';
      obs.observe(s);
    });
    return () => obs.disconnect();
  }, []);

  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/api/login/';
  };

  return (
    <div className={styles.page}>
      <div className={styles.container}>

        {/* ── Hero ── */}
        <header className={styles.hero}>
          <div className={styles.badge}>
            <span className={styles.blink} />
            Fall 2024 · Personal Project
          </div>
          <h1 className={styles.h1}>
            Spotify<br /><span>Personality Type</span>
          </h1>
          <p className={styles.subtitle}>
            Analyze your Spotify listening data to generate unique personality insights powered by your music taste.
          </p>
          <div className={styles.heroTags}>
            {['Django','React','MySQL','Spotify OAuth','REST API','Python'].map(t => (
              <span key={t} className={styles.tag}>{t}</span>
            ))}
          </div>
          {error && (
            <div className={styles.error}>⚠️ Auth error: {error}. Please try again.</div>
          )}
          <div className={styles.ctaRow}>
            <button className={styles.btnPrimary} onClick={handleLogin}>
              <span>🎧</span> Connect with Spotify
            </button>
            <a href="#how" className={styles.btnGhost}>
              <span>↓</span> How it works
            </a>
          </div>
        </header>

        {/* ── Stats ── */}
        <div className={styles.statsBar} data-fade>
          <div className={styles.stat}><span className={styles.statVal}>10+</span><span className={styles.statLabel}>Active Users</span></div>
          <div className={styles.stat}><span className={styles.statVal}>OAuth2</span><span className={styles.statLabel}>Auth Method</span></div>
          <div className={styles.stat}><span className={styles.statVal}>16</span><span className={styles.statLabel}>Personality Types</span></div>
        </div>

        {/* ── Features ── */}
        <section data-fade id="how">
          <div className={styles.sectionLabel}>Features</div>
          <h2 className={styles.h2}>What it does</h2>
          <div className={styles.featureGrid}>
            {FEATURES.map(f => (
              <div key={f.title} className={styles.featureCard}>
                <div className={styles.featureIcon}>{f.icon}</div>
                <div className={styles.featureTitle}>{f.title}</div>
                <div className={styles.featureDesc}>{f.desc}</div>
              </div>
            ))}
          </div>
        </section>

        {/* ── Architecture ── */}
        <section data-fade>
          <div className={styles.sectionLabel}>Architecture</div>
          <h2 className={styles.h2}>How it's built</h2>
          <div className={styles.archDiagram}>
            {[
              { icon: '🎧', name: 'Spotify API', sub: 'OAuth 2.0' },
              { icon: '🐍', name: 'Django',      sub: 'REST Backend' },
              { icon: '🗄️', name: 'MySQL',       sub: 'Data Store' },
              { icon: '⚛️', name: 'React',       sub: 'Frontend' },
            ].map((n, i, arr) => (
              <div key={n.name} style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
                <div className={styles.archNode}>
                  <div className={styles.archNodeIcon}>{n.icon}</div>
                  <div className={styles.archNodeName}>{n.name}</div>
                  <div className={styles.archNodeSub}>{n.sub}</div>
                </div>
                {i < arr.length - 1 && <div className={styles.archArrow}>→</div>}
              </div>
            ))}
          </div>
        </section>

        {/* ── Stack ── */}
        <section data-fade>
          <div className={styles.sectionLabel}>Tech Stack</div>
          <h2 className={styles.h2}>Built with</h2>
          <div className={styles.stackGrid}>
            {STACK.map(s => (
              <div key={s.name} className={styles.stackItem}>
                <div className={styles.stackIcon} style={{ background: s.bg }}>{s.icon}</div>
                <div>
                  <div className={styles.stackName}>{s.name}</div>
                  <div className={styles.stackRole}>{s.role}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── CTA ── */}
        <section data-fade className={styles.ctaSection}>
          <div className={styles.sectionLabel}>Get Started</div>
          <h2 className={styles.h2}>Ready to discover your type?</h2>
          <p className={styles.subtitle} style={{ marginBottom: 32 }}>
            Connect your Spotify account. It only takes a few seconds.
          </p>
          <button className={styles.btnPrimary} onClick={handleLogin} style={{ fontSize: 16, padding: '14px 32px' }}>
            <span>🎧</span> Connect with Spotify
          </button>
        </section>

        <footer className={styles.footer}>
          <p>Built with ♥ · Fall 2024 · Django · React · MySQL · Spotify Web API</p>
        </footer>
      </div>
    </div>
  );
}
