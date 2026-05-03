// ── Screen 4: Loading & Screen 5: Error states ──
const { useState: useStateL, useEffect: useEffectL, useRef: useRefL } = React;

const LOADING_STEPS = [
  { id: 1, label: 'Blizzard API에서 장비 정보를 불러오는 중...',  hint: 'FETCHING ARMORY' },
  { id: 2, label: '상위 1% 유저 데이터와 비교하는 중...',         hint: 'BENCHMARKING' },
  { id: 3, label: '스텟 갭을 계산하는 중...',                      hint: 'CALCULATING GAP' },
  { id: 4, label: '최적 아이템을 추천하는 중...',                  hint: 'RANKING ITEMS' },
];

function LoadingScreen({ charName = '아즈모단', realm = '아즈샤라', onCancel }) {
  const [step, setStep] = useStateL(0);
  const [progress, setProgress] = useStateL(0);
  const t = useRefL(null);

  useEffectL(() => {
    let p = 0;
    t.current = setInterval(() => {
      p += 0.6;
      if (p >= 100) p = 100;
      setProgress(p);
      const s = Math.min(LOADING_STEPS.length - 1, Math.floor(p / 25));
      setStep(s);
      if (p >= 100) clearInterval(t.current);
    }, 60);
    return () => clearInterval(t.current);
  }, []);

  const ringR = 86;
  const ringC = 2 * Math.PI * ringR;
  const dash = (progress / 100) * ringC;

  return (
    <div className="loading-screen page-enter">
      <div className="loading-logo">
        <span className="logo-mark">
          <svg width="24" height="24" viewBox="0 0 32 32" fill="none">
            <path d="M16 2 L28 9 L28 23 L16 30 L4 23 L4 9 Z"
                  stroke="var(--gold)" strokeWidth="1.2" fill="oklch(0.22 0.014 65)" />
            <circle cx="16" cy="16" r="2.5" fill="var(--gold)" />
          </svg>
        </span>
        <span style={{ fontFamily: 'Cinzel, serif', fontSize: 14, letterSpacing: '0.16em',
                       textTransform: 'uppercase', color: 'var(--text-dim)' }}>
          Gear<span style={{ color: 'var(--gold)' }}>Gap</span>
        </span>
      </div>

      <div className="loading-target">
        <div className="lt-line">
          <span className="lt-name">{charName}</span>
          <span className="lt-sep">·</span>
          <span className="lt-realm">{realm}</span>
        </div>
        <div className="lt-status">분석 중<span className="lt-dots"><span></span><span></span><span></span></span></div>
      </div>

      <div className="ring-wrap">
        <svg className="ring-runic" viewBox="0 0 240 240">
          <circle cx="120" cy="120" r="115" fill="none" stroke="oklch(0.34 0.014 65)" strokeWidth="1" strokeDasharray="2 6" />
          <g className="runic-spin">
            {Array.from({ length: 12 }).map((_, i) => {
              const a = (i / 12) * Math.PI * 2;
              const x = 120 + Math.cos(a) * 105;
              const y = 120 + Math.sin(a) * 105;
              return <circle key={i} cx={x} cy={y} r="1.6" fill="var(--gold-deep)" />;
            })}
          </g>
        </svg>

        <svg className="ring-prog" viewBox="0 0 200 200">
          <circle cx="100" cy="100" r={ringR} fill="none" stroke="var(--border-soft)" strokeWidth="2" />
          <circle cx="100" cy="100" r={ringR} fill="none"
            stroke="url(#gold-grad)" strokeWidth="3" strokeLinecap="round"
            strokeDasharray={`${dash} ${ringC}`}
            transform="rotate(-90 100 100)"
            style={{ transition: 'stroke-dasharray 0.18s linear', filter: 'drop-shadow(0 0 6px oklch(0.66 0.13 65 / 0.5))' }} />
          <defs>
            <linearGradient id="gold-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="oklch(0.85 0.135 78)" />
              <stop offset="100%" stopColor="oklch(0.62 0.13 60)" />
            </linearGradient>
          </defs>
        </svg>

        <div className="ring-center">
          <div className="ring-pct">{Math.floor(progress)}<span>%</span></div>
          <div className="ring-step">STEP {step + 1} / 4</div>
        </div>
      </div>

      <div className="loading-steps">
        {LOADING_STEPS.map((s, i) => {
          const state = i < step ? 'done' : i === step ? 'active' : 'pending';
          return (
            <div key={s.id} className={`lstep ${state}`}>
              <div className="lstep-bullet">
                {state === 'done' && (
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path d="M2 5L4 7L8 3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                )}
                {state === 'active' && <span className="lstep-spin"></span>}
                {state === 'pending' && <span className="lstep-dot"></span>}
              </div>
              <div className="lstep-text">
                <div className="lstep-hint">{s.hint}</div>
                <div className="lstep-label">{s.label}</div>
              </div>
              <div className="lstep-time">
                {state === 'done' && '완료'}
                {state === 'active' && '진행 중'}
                {state === 'pending' && '대기'}
              </div>
            </div>
          );
        })}
      </div>

      <button className="loading-cancel" onClick={onCancel}>
        분석 취소
      </button>
    </div>
  );
}

// ── Error screen ──
function ErrorIcon({ kind }) {
  if (kind === 'notfound') {
    return (
      <svg viewBox="0 0 64 64" fill="none">
        <circle cx="32" cy="32" r="26" stroke="currentColor" strokeWidth="1.4" strokeDasharray="3 4" />
        <circle cx="32" cy="24" r="6" stroke="currentColor" strokeWidth="1.6" />
        <path d="M20 46c2.5-7 6-10 12-10s9.5 3 12 10" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
        <text x="44" y="22" fontFamily="Cinzel" fontSize="14" fontWeight="700" fill="currentColor">?</text>
      </svg>
    );
  }
  if (kind === 'api') {
    return (
      <svg viewBox="0 0 64 64" fill="none">
        <rect x="14" y="12" width="36" height="14" rx="1" stroke="currentColor" strokeWidth="1.6" />
        <rect x="14" y="38" width="36" height="14" rx="1" stroke="currentColor" strokeWidth="1.6" />
        <circle cx="20" cy="19" r="1.5" fill="currentColor" />
        <circle cx="20" cy="45" r="1.5" fill="currentColor" />
        <line x1="26" y1="19" x2="42" y2="19" stroke="currentColor" strokeWidth="1.4" />
        <line x1="26" y1="45" x2="42" y2="45" stroke="currentColor" strokeWidth="1.4" />
        <path d="M34 28 L28 36 L34 36 L30 44" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 64 64" fill="none">
      <path d="M32 8 L50 16 L50 32 C50 42 42 50 32 56 C22 50 14 42 14 32 L14 16 Z"
            stroke="currentColor" strokeWidth="1.6" fill="none" />
      <path d="M32 20 L40 24 L40 32 C40 38 36 42 32 44 C28 42 24 38 24 32 L24 24 Z"
            stroke="currentColor" strokeWidth="1.2" fill="none" />
      <line x1="22" y1="50" x2="42" y2="14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeDasharray="3 3" />
    </svg>
  );
}

const ERROR_CASES = [
  {
    kind: 'notfound',
    code: '404 · NOT FOUND',
    title: '캐릭터를 찾을 수 없어요',
    desc: '캐릭터명 또는 서버를 다시 확인해주세요. 대소문자 또는 한글/영문 표기가 정확한지 살펴봐 주세요.',
    primary: { label: '다시 검색하기', action: 'search' },
    accent: 'gold',
  },
  {
    kind: 'api',
    code: '503 · SERVICE UNAVAILABLE',
    title: '데이터를 불러오지 못했어요',
    desc: 'Blizzard 서버가 일시적으로 응답하지 않아요. 잠시 후 다시 시도해주세요.',
    primary: { label: '다시 시도하기', action: 'retry' },
    secondary: { label: '메인으로', action: 'search' },
    accent: 'crimson',
  },
  {
    kind: 'unsupported',
    code: 'WIP · COMING SOON',
    title: '아직 지원하지 않는 스펙이에요',
    desc: '현재 흑마법사(파멸 / 고통 / 악마소환)만 지원해요. 더 많은 직업을 준비 중이에요!',
    primary: { label: '다시 검색하기', action: 'search' },
    accent: 'steel',
  },
];

const ACCENT_COLOR = {
  gold: 'var(--gold)',
  crimson: 'var(--crimson)',
  steel: 'var(--steel)',
};

function ErrorCard({ c, onAction }) {
  const accent = ACCENT_COLOR[c.accent];
  return (
    <div className="err-card" style={{ '--accent': accent }}>
      <div className="err-corner tl"></div>
      <div className="err-corner tr"></div>
      <div className="err-corner bl"></div>
      <div className="err-corner br"></div>

      <div className="err-code">{c.code}</div>
      <div className="err-icon"><ErrorIcon kind={c.kind} /></div>
      <div className="err-title">{c.title}</div>
      <div className="err-desc">{c.desc}</div>

      <div className="err-actions">
        <button className="err-btn primary" onClick={() => onAction(c.primary.action)}>
          {c.primary.label}
        </button>
        {c.secondary && (
          <button className="err-btn secondary" onClick={() => onAction(c.secondary.action)}>
            {c.secondary.label}
          </button>
        )}
      </div>
    </div>
  );
}

function ErrorScreen({ onAction }) {
  const handle = onAction || ((a) => {
    if (a === 'search') window.__nav('landing');
    if (a === 'retry') window.__nav('loading');
  });
  return (
    <div className="page-enter" style={{ paddingTop: 24 }}>
      <div className="page-header">
        <div className="crumbs">
          <a onClick={() => window.__nav('landing')}>Search</a>
          <span className="sep">/</span>
          <span className="here">Errors · State Reference</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
                      flexWrap: 'wrap', gap: 16 }}>
          <h1 style={{ fontFamily: 'Cinzel, serif', fontSize: 32, fontWeight: 600,
                       letterSpacing: '0.04em', margin: 0 }}>
            Error States
          </h1>
          <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 11,
                        color: 'var(--text-mute)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            3 · 케이스별 안내 · 친근한 톤 유지
          </div>
        </div>
      </div>

      <div className="err-grid">
        {ERROR_CASES.map((c) => (
          <ErrorCard key={c.kind} c={c} onAction={handle} />
        ))}
      </div>

      <div className="err-foot">
        <span style={{ color: 'var(--text-mute)' }}>모든 에러는 같은 톤 + 동일 레이아웃 그리드를 따릅니다.</span>
        <span style={{ color: 'var(--gold)' }}>Discord 에서 더 많은 도움 받기 →</span>
      </div>
    </div>
  );
}

window.LoadingScreen = LoadingScreen;
window.ErrorScreen = ErrorScreen;
