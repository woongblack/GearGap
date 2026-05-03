// ── Main app shell — handles screen routing & landing screen ──
const { useState, useEffect, useRef } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accentHue": 78,
  "headlineFont": "Cinzel",
  "showSigil": true,
  "showStats": true,
  "characterCount": 4
}/*EDITMODE-END*/;

const ROLE_COLOR = {
  'dps-arcane': 'var(--steel)',
  'dps-warlock': 'var(--violet)',
  'healer': 'var(--jade)',
  'tank': 'var(--violet)',
  'dps-melee': 'var(--crimson)',
};
const GAP_COLOR = {
  gold: 'var(--gold)',
  jade: 'var(--jade)',
  crimson: 'var(--crimson)',
};

// ── Tiny logo mark ──
function LogoMark() {
  return (
    <span className="logo-mark">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <path d="M16 2 L28 9 L28 23 L16 30 L4 23 L4 9 Z"
              stroke="var(--gold)" strokeWidth="1.2" fill="oklch(0.22 0.014 65)" />
        <path d="M16 8 L23 12 L23 20 L16 24 L9 20 L9 12 Z"
              stroke="var(--gold-deep)" strokeWidth="0.8" fill="none" />
        <circle cx="16" cy="16" r="2.5" fill="var(--gold)" />
        <path d="M16 11 L16 14 M16 18 L16 21 M11 16 L14 16 M18 16 L21 16"
              stroke="var(--gold)" strokeWidth="1" />
      </svg>
    </span>
  );
}

function Topbar({ active, onNav }) {
  return (
    <nav className="topbar">
      <a className="logo" onClick={() => onNav('landing')} style={{ cursor: 'pointer' }}>
        <LogoMark />
        <span>Gear<span className="logo-gap">Gap</span></span>
      </a>
      <div className="nav-links">
        <a onClick={() => onNav('landing')} className={active === 'landing' ? 'active' : ''} style={{ cursor: 'pointer' }}>Search</a>
        <a onClick={() => onNav('analysis')} className={active === 'analysis' ? 'active' : ''} style={{ cursor: 'pointer' }}>Analysis</a>
        <a onClick={() => onNav('recs')} className={active === 'recs' ? 'active' : ''} style={{ cursor: 'pointer' }}>Compare</a>
        <a>Leaderboards</a>
        <button className="nav-cta">Sign In</button>
      </div>
    </nav>
  );
}

function SearchForm({ onSubmit }) {
  const [name, setName] = useState('');
  const [realm, setRealm] = useState('azshara');
  function submit(e) {
    e.preventDefault();
    if (!name.trim()) return;
    onSubmit({ name: name.trim(), realm });
  }
  return (
    <div className="search-panel">
      <span className="search-corner-tr"></span>
      <span className="search-corner-bl"></span>
      <form className="search-form" onSubmit={submit}>
        <label className="field">
          <span className="field-label">Character</span>
          <input type="text" placeholder="캐릭터명을 입력하세요" value={name}
                 onChange={(e) => setName(e.target.value)} autoComplete="off" />
        </label>
        <label className="field">
          <span className="field-label">Realm · KR</span>
          <select value={realm} onChange={(e) => setRealm(e.target.value)}>
            {window.GG_DATA.REALMS.map((r) => (
              <option key={r.value} value={r.value}>{r.label}</option>
            ))}
          </select>
        </label>
        <button type="submit" className="search-btn">
          <svg viewBox="0 0 16 16" fill="none">
            <circle cx="7" cy="7" r="5" stroke="currentColor" strokeWidth="1.6"/>
            <path d="M11 11 L14 14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
          </svg>
          Analyze
        </button>
      </form>
    </div>
  );
}

function CharacterCard({ c, onClick }) {
  const color = ROLE_COLOR[c.role];
  const gapColor = GAP_COLOR[c.gapColor];
  return (
    <div className="char-card" style={{ '--class-color': color, '--gap-color': gapColor }}
         onClick={onClick}>
      <div className="char-gap"><span className="arrow">↗</span><span>{c.gap}</span></div>
      <div className="char-top">
        <div className="char-portrait">{c.initial}</div>
        <div className="char-info">
          <div className="char-name">{c.name}</div>
          <div className="char-spec">{c.spec}</div>
        </div>
      </div>
      <div className="char-meta">
        <div>
          <span className="char-ilvl"><span className="lbl">item lvl</span>{c.ilvl}</span>
        </div>
        <div className="char-server">
          <div className="char-server-name">{c.realm}</div>
          <div className="char-server-ts">{c.when}</div>
        </div>
      </div>
    </div>
  );
}

function Toast({ msg, show }) {
  return (
    <div className={`toast ${show ? 'show' : ''}`}>
      <span className="spin"></span><span>{msg}</span>
    </div>
  );
}

function LandingScreen({ tweaks, onSearch }) {
  const D = window.GG_DATA;
  const visible = D.RECENT.slice(0, tweaks.characterCount);
  return (
    <div className="page-enter">
      <section className="hero">
        <span className="eyebrow">
          <span className="dot"></span>
          Patch 11.1 · Season of Ascension
        </span>
        <h1 className="title">
          Find Your <span className="accent">Gear Gap</span>
        </h1>
        <p className="subtitle">
          상위 <span className="em">1%</span> 템셋 데이터 기반으로 당신의 장비를 분석하고,
          가장 효율적인 <span className="em">레이드 넴드</span>와 <span className="em">쐐기 던전</span>을 추천합니다.
        </p>
        <SearchForm onSubmit={onSearch} />
        {tweaks.showStats && (
          <div className="stat-strip">
            <div className="stat"><div className="stat-num">2.4M</div><div className="stat-label">Characters Indexed</div></div>
            <div className="stat"><div className="stat-num">14</div><div className="stat-label">Raid Bosses Tracked</div></div>
            <div className="stat"><div className="stat-num">8</div><div className="stat-label">M+ Dungeons</div></div>
            <div className="stat"><div className="stat-num">11.1.5</div><div className="stat-label">Live Patch</div></div>
          </div>
        )}
      </section>
      <section className="section">
        <div className="section-head">
          <div className="section-title">
            <span className="ornament"></span>
            <h2>Recent Searches</h2>
            <span className="ornament"></span>
          </div>
          <a className="section-link" style={{ cursor: 'pointer' }}>View All →</a>
        </div>
        <div className="recent-grid">
          {visible.map((c) => <CharacterCard key={c.name} c={c} onClick={() => window.__nav('analysis')} />)}
        </div>
      </section>
    </div>
  );
}

function ScreenSwitcher({ active, onNav }) {
  return (
    <div className="screen-switcher">
      <button className={active === 'landing' ? 'active' : ''} onClick={() => onNav('landing')}>1 · Search</button>
      <button className={active === 'loading' ? 'active' : ''} onClick={() => onNav('loading')}>2 · Loading</button>
      <button className={active === 'analysis' ? 'active' : ''} onClick={() => onNav('analysis')}>3 · Analysis</button>
      <button className={active === 'recs' ? 'active' : ''} onClick={() => onNav('recs')}>4 · Compare</button>
      <button className={active === 'errors' ? 'active' : ''} onClick={() => onNav('errors')}>5 · Errors</button>
    </div>
  );
}

function App() {
  const [tweaks, setTweak] = window.useTweaks(TWEAK_DEFAULTS);
  const [screen, setScreen] = useState('landing');
  const [toast, setToast] = useState({ show: false, msg: '' });
  const [metaOpen, setMetaOpen] = useState(false);
  const toastTimer = useRef(null);

  useEffect(() => {
    window.__nav = (s) => {
      setScreen(s);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };
  }, []);

  useEffect(() => {
    const h = tweaks.accentHue;
    document.documentElement.style.setProperty('--gold', `oklch(0.80 0.135 ${h})`);
    document.documentElement.style.setProperty('--gold-deep', `oklch(0.66 0.13 ${h - 13})`);
    document.documentElement.style.setProperty('--gold-soft', `oklch(0.45 0.08 ${h - 8})`);
  }, [tweaks.accentHue]);

  useEffect(() => {
    document.querySelectorAll('h1.title, .logo, .section-title h2, .char-name, .char-ilvl, .stat-num, .search-btn, .ch-name, .panel-head h3, .boss-name, .boss-num, .item-ilvl, .ch-stat .v, .ch-score .pct, .gs-cell .v, .dgn-score-num, .slot-ilvl, .cta-title, .cta-btn, .tab')
      .forEach(el => { el.style.fontFamily = `'${tweaks.headlineFont}', serif`; });
  }, [tweaks.headlineFont, screen]);

  function handleSearch({ name, realm }) {
    const realmLabel = window.GG_DATA.REALMS.find(r => r.value === realm)?.label || realm;
    setToast({ show: true, msg: `Scanning ${name} · ${realmLabel} …` });
    clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => {
      setToast(t => ({ ...t, show: false }));
      setScreen('loading');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 900);
  }

  return (
    <>
      <div className="shell" data-screen-label={
        screen === 'landing' ? '01 Landing' :
        screen === 'loading' ? '02 Loading' :
        screen === 'analysis' ? '03 Analysis' :
        screen === 'recs' ? '04 Compare' :
        '05 Errors'
      }>
        <Topbar active={screen} onNav={(s) => window.__nav(s)} />

        {(screen === 'analysis' || screen === 'recs') && (
          <div style={{ maxWidth: 1320, margin: '0 auto', padding: '20px 24px 0' }}>
            <window.MetaRibbon onOpen={() => setMetaOpen(true)} />
          </div>
        )}

        {screen === 'landing' && <LandingScreen tweaks={tweaks} onSearch={handleSearch} />}
        {screen === 'loading' && <window.LoadingScreen onCancel={() => window.__nav('landing')} />}
        {screen === 'analysis' && <window.AnalysisScreen onAnalyze={() => window.__nav('recs')} />}
        {screen === 'recs' && <window.RecommendationsScreen />}
        {screen === 'errors' && <window.ErrorScreen />}

        <window.MetaDrawer open={metaOpen} onClose={() => setMetaOpen(false)} />

        <footer>
          <span className="legal">© 2026 GearGap · v0.4.2</span>
          <div className="links">
            <a>About</a><a>API</a><a>Discord</a><a>Changelog</a>
          </div>
        </footer>
      </div>

      <ScreenSwitcher active={screen} onNav={(s) => window.__nav(s)} />
      <Toast msg={toast.msg} show={toast.show} />

      <window.TweaksPanel title="Tweaks">
        <window.TweakSection label="Aesthetic">
          <window.TweakSlider label="Accent hue" value={tweaks.accentHue}
            min={0} max={360} step={1} onChange={(v) => setTweak('accentHue', v)} />
          <window.TweakSelect label="Headline font" value={tweaks.headlineFont}
            options={[
              { value: 'Cinzel', label: 'Cinzel (default)' },
              { value: 'Inter', label: 'Inter (sans)' },
              { value: 'JetBrains Mono', label: 'JetBrains Mono' },
            ]}
            onChange={(v) => setTweak('headlineFont', v)} />
        </window.TweakSection>
        <window.TweakSection label="Layout">
          <window.TweakToggle label="Show stats strip"
            value={tweaks.showStats} onChange={(v) => setTweak('showStats', v)} />
          <window.TweakSlider label="Recent characters"
            value={tweaks.characterCount} min={1} max={4} step={1}
            onChange={(v) => setTweak('characterCount', v)} />
        </window.TweakSection>
      </window.TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
