interface ErrorIconProps {
  kind: 'notfound' | 'api' | 'unsupported';
}

function ErrorIcon({ kind }: ErrorIconProps) {
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

export interface ErrorCase {
  kind: 'notfound' | 'api' | 'unsupported';
  code: string;
  title: string;
  desc: string;
  primary: { label: string; action: string };
  secondary?: { label: string; action: string };
  accent: 'gold' | 'crimson' | 'steel';
}

const ACCENT_COLOR = {
  gold: 'var(--gold)',
  crimson: 'var(--crimson)',
  steel: 'var(--steel)',
};

interface ErrorCardProps {
  c: ErrorCase;
  onAction: (action: string) => void;
}

export default function ErrorCard({ c, onAction }: ErrorCardProps) {
  const accent = ACCENT_COLOR[c.accent];
  return (
    <div className="err-card" style={{ '--accent': accent } as React.CSSProperties}>
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
        {c.secondary ? (
          <button className="err-btn secondary" onClick={() => onAction(c.secondary!.action)}>
            {c.secondary.label}
          </button>
        ) : null}
      </div>
    </div>
  );
}
