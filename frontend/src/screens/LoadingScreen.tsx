import { useState, useEffect, useRef } from 'react';

const LOADING_STEPS = [
  { id: 1, label: 'Blizzard API에서 장비 정보를 불러오는 중...',  hint: 'FETCHING ARMORY' },
  { id: 2, label: '상위 1% 유저 데이터와 비교하는 중...',         hint: 'BENCHMARKING' },
  { id: 3, label: '스텟 갭을 계산하는 중...',                      hint: 'CALCULATING GAP' },
  { id: 4, label: '최적 아이템을 추천하는 중...',                  hint: 'RANKING ITEMS' },
];

interface LoadingScreenProps {
  charName?: string;
  realm?: string;
  onCancel: () => void;
  onComplete?: () => void;
}

export default function LoadingScreen({ charName = '아즈모단', realm = '아즈샤라', onCancel, onComplete }: LoadingScreenProps) {
  const [step, setStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const t = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let p = 0;
    t.current = setInterval(() => {
      p += 0.6;
      if (p >= 100) p = 100;
      setProgress(p);
      const s = Math.min(LOADING_STEPS.length - 1, Math.floor(p / 25));
      setStep(s);
      if (p >= 100) {
        if (t.current) clearInterval(t.current);
        if (onComplete) onComplete();
      }
    }, 60);
    return () => {
      if (t.current) clearInterval(t.current);
    };
  }, [onComplete]);

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
