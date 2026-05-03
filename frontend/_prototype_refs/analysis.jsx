// ── Screen 2: Character Analysis ──
const { useState: useStateA, useMemo: useMemoA } = React;

function StatRadar({ stats }) {
  const size = 360;
  const cx = size / 2, cy = size / 2;
  const radius = 130;
  const n = stats.length;
  const angleFor = (i) => (Math.PI * 2 * i / n) - Math.PI / 2;

  // Normalize: max display = 1.15 × target (so target sits ~0.87 on the axis)
  const maxFor = (s) => s.target * 1.15;

  const pt = (i, ratio) => {
    const a = angleFor(i);
    return [cx + Math.cos(a) * radius * ratio, cy + Math.sin(a) * radius * ratio];
  };

  const targetPath = stats.map((s, i) => pt(i, s.target / maxFor(s))).map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ') + ' Z';
  const currentPath = stats.map((s, i) => pt(i, s.current / maxFor(s))).map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ') + ' Z';

  const rings = [0.25, 0.5, 0.75, 1.0];
  const ringPath = (r) => stats.map((_, i) => pt(i, r)).map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ') + ' Z';

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="radar-svg" aria-label="Stat radar">
      <g className="radar-grid">
        {rings.map((r, i) => <polygon key={i} points={stats.map((_, j) => pt(j, r).join(',')).join(' ')} />)}
        {stats.map((_, i) => {
          const [x, y] = pt(i, 1);
          return <line key={i} x1={cx} y1={cy} x2={x} y2={y} />;
        })}
      </g>
      <path className="radar-target" d={targetPath} />
      <path className="radar-current" d={currentPath} />
      {stats.map((s, i) => {
        const [x, y] = pt(i, s.current / maxFor(s));
        return <circle key={i} className="radar-current-pt" cx={x} cy={y} r={3.5} />;
      })}
      {stats.map((s, i) => {
        const [x, y] = pt(i, 1.18);
        return (
          <text key={i} x={x} y={y} className="radar-axis-label"
                textAnchor="middle" dominantBaseline="middle">
            {s.short}
          </text>
        );
      })}
    </svg>
  );
}

function StatBars({ stats }) {
  return (
    <div className="stat-bars">
      {stats.map((s) => {
        const max = s.target * 1.15;
        const curPct = (s.current / max) * 100;
        const tgtPct = (s.target / max) * 100;
        const gap = +(s.target - s.current).toFixed(1);
        const high = gap >= 5;
        return (
          <div key={s.key} className={`stat-row ${high ? 'high' : ''}`}>
            <span className="name">{s.short}</span>
            <div className="stat-track">
              <div className="stat-fill" style={{ width: `${curPct}%` }}></div>
              <div className="stat-target-mark" style={{ left: `calc(${tgtPct}% - 1px)` }}></div>
            </div>
            <div className="stat-vals">
              <span className="cur">{s.current}{s.unit}</span>
              <span className={`gap ${high ? 'high' : ''}`}>−{gap}{s.unit}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

const SLOT_LABELS = {
  head: 'HEAD', neck: 'NECK', shoulder: 'SHOULDER', cloak: 'BACK', chest: 'CHEST',
  wrist: 'WRIST', hands: 'HANDS', waist: 'WAIST', legs: 'LEGS', feet: 'FEET',
  ring1: 'RING I', ring2: 'RING II', trinket1: 'TRINKET I', trinket2: 'TRINKET II',
  mainhand: 'MAIN', offhand: 'OFF',
};

function SlotRow({ s }) {
  const gapClass = s.gap === 0 ? 'zero' : s.gap >= 10 ? 'high' : 'med';
  const barW = Math.min(100, s.gap * 5);
  return (
    <div className={`slot-row ${s.hot ? 'hot' : ''}`}>
      <span className="slot-icon">{s.ko[0]}</span>
      <span className="slot-name">{SLOT_LABELS[s.slot] || s.slot}</span>
      <div className="slot-item">
        <div>{s.name}</div>
        <div className="src">{s.source}</div>
      </div>
      <span className="slot-ilvl">{s.ilvl || '—'}</span>
      <div className={`slot-gap-ind ${gapClass}`}>
        <div className="slot-gap-bar"><span style={{ width: `${barW}%` }}></span></div>
        <span className="val">{s.gap === 0 ? '0' : `+${s.gap}`}</span>
      </div>
    </div>
  );
}

function CharHeader({ char }) {
  return (
    <div className="char-header">
      <div className="ch-portrait">
        <span className="corner tl"></span><span className="corner tr"></span>
        <span className="corner bl"></span><span className="corner br"></span>
        {char.avatarInitial}
      </div>
      <div className="ch-meta">
        <div className="ch-name">{char.name}</div>
        <div className="ch-tags">
          <span className="ch-tag spec">{char.classSpec}</span>
          <span className="ch-tag">Lv {char.level}</span>
          <span className="ch-tag">{char.realm} · {char.region}</span>
          <span className="ch-tag">갱신 {char.lastUpdated}</span>
        </div>
        <div className="ch-row">
          <div className="ch-stat">
            <span className="l">Item Level</span>
            <span className="v gold">{char.ilvl.toFixed(1)}</span>
          </div>
          <div className="ch-stat">
            <span className="l">GearGap Score</span>
            <span className="v">{char.score}</span>
          </div>
          <div className="ch-stat">
            <span className="l">Class</span>
            <span className="v" style={{ fontSize: 16 }}>{char.classKo}</span>
          </div>
        </div>
      </div>
      <div className="ch-score">
        <div className="pct"><sup>TOP</sup>{char.percentile}%</div>
        <div className="lab">Percentile · KR</div>
        <div className="sub">상위 1% 까지 17 ilvl</div>
      </div>
    </div>
  );
}

function AnalysisScreen({ onAnalyze }) {
  const D = window.GG_DATA;
  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="crumbs">
          <a onClick={() => window.__nav('landing')}>Search</a>
          <span className="sep">/</span>
          <span className="here">Analysis</span>
          <span className="sep">/</span>
          <span>{D.CHAR.name} · {D.CHAR.realm}</span>
        </div>
        <CharHeader char={D.CHAR} />
      </div>

      <div className="analysis-grid">
        <div className="panel">
          <div className="panel-head">
            <h3>Stat Gap</h3>
            <span className="hint">현재 vs 상위 1%</span>
          </div>
          <div className="radar-wrap">
            <StatRadar stats={D.STATS} />
          </div>
          <div className="radar-legend">
            <span><span className="swatch cur"></span>Current</span>
            <span><span className="swatch tgt"></span>Top 1% Target</span>
          </div>
          <StatBars stats={D.STATS} />
        </div>

        <div className="panel">
          <div className="panel-head">
            <h3>Slot Gap</h3>
            <span className="hint">우선순위 3개 강조</span>
          </div>
          <div className="slot-list">
            {D.SLOTS.map((s) => <SlotRow key={s.slot} s={s} />)}
          </div>
        </div>
      </div>

      <div className="cta-bar">
        <div className="cta-text">
          <div className="cta-title">3개 슬롯에서 큰 갭이 발견되었습니다</div>
          <div className="cta-sub">
            레이드·쐐기 경로별 <b>예상 gain</b>·<b>시간 비용</b>·<b>드랍 확률</b>을 한 표에 모아드립니다.
          </div>
        </div>
        <button className="cta-btn" onClick={onAnalyze}>
          경로 비교하기
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}

window.AnalysisScreen = AnalysisScreen;
window.CharHeader = CharHeader;
