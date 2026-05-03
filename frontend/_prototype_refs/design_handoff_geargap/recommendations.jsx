// ── Screen 3: Recommendations (Raid + Mythic+) ──
const { useState: useStateR } = React;

function DiffBadge({ d }) {
  const D = window.GG_DATA.DIFFICULTY[d];
  return <span className="diff-badge" style={{ color: D.color }}>{D.ko}</span>;
}

function PriorityBadge({ p }) {
  const labels = { high: 'HIGH PRIORITY', med: 'MEDIUM', low: 'LOW' };
  return (
    <span className={`priority-badge ${p}`}>
      <span className="pdot"></span>
      <span>{labels[p]}</span>
    </span>
  );
}

function ItemTooltip({ item, ilvl, slot }) {
  return (
    <div className="item-tip">
      <div className="tip-name">{item}</div>
      <div className="tip-meta">{slot} · ILVL {ilvl} · EPIC</div>
      <div className="tip-stat"><span>지능</span><span className="vv">+1,842</span></div>
      <div className="tip-stat"><span>체력</span><span className="vv">+24,610</span></div>
      <div className="tip-divider"></div>
      <div className="tip-stat"><span>특화</span><span className="vv">+312</span></div>
      <div className="tip-stat"><span>신속</span><span className="vv">+185</span></div>
      <div className="tip-divider"></div>
      <div className="tip-flavor">"잿불에 단련된 자만이 이 형상을 견디리라."</div>
    </div>
  );
}

function BossCard({ b }) {
  return (
    <div className={`boss-card ${b.priority}`}>
      <div className="boss-top">
        <div className="boss-num">{String(b.idx).padStart(2, '0')}</div>
        <div className="boss-info">
          <div className="boss-name">{b.name}</div>
          <div className="boss-name-en">{b.nameEn}</div>
        </div>
        <div className="boss-meta">
          <PriorityBadge p={b.priority} />
          <DiffBadge d={b.difficulty} />
        </div>
      </div>
      <div className="boss-item tt-anchor">
        <div className="item-icon">{b.slot[0]}</div>
        <div className="item-mid">
          <div className="item-name">{b.item}</div>
          <div className="item-sub">
            {b.slot}<span className="dot">·</span>{window.GG_DATA.RAID.name}
          </div>
        </div>
        <div className="item-ilvl">
          <span className="l">ilvl</span>
          {b.ilvl}
        </div>
        <ItemTooltip item={b.item} ilvl={b.ilvl} slot={b.slot} />
      </div>
      <div className="boss-why">
        <span className="ai">AI</span>
        <span>{b.why}</span>
        <span className="boss-gain">
          <span className="arrow">↑</span>
          {b.stat} {b.gain}%
        </span>
      </div>
    </div>
  );
}

function DungeonCard({ d }) {
  const tier = d.score >= 70 ? 'high' : d.score >= 50 ? 'med' : 'low';
  return (
    <div className={`boss-card ${tier}`}>
      <div className="boss-top">
        <div className="boss-num">{String(d.idx).padStart(2, '0')}</div>
        <div className="boss-info">
          <div className="boss-name">{d.name}</div>
          <div className="boss-name-en">{d.nameEn} · {d.drop}</div>
        </div>
        <div className="boss-meta">
          <span className="priority-badge" style={{ color: 'var(--gold)' }}>
            <span className="pdot"></span>{d.key}
          </span>
        </div>
      </div>
      <div className="boss-item tt-anchor">
        <div className="item-icon">{d.slot[0]}</div>
        <div className="item-mid">
          <div className="item-name">{d.item}</div>
          <div className="item-sub">
            {d.slot}<span className="dot">·</span>{d.drop}
          </div>
        </div>
        <div className="item-ilvl">
          <span className="l">ilvl</span>
          {d.ilvl}
        </div>
        <ItemTooltip item={d.item} ilvl={d.ilvl} slot={d.slot} />
      </div>
      <div className="boss-why">
        <span className="ai">AI</span>
        <span>{d.why}</span>
        <span className="boss-gain">
          <span className="arrow">↑</span>
          {d.stat} {d.gain}%
        </span>
      </div>
      <div className="dgn-score">
        <span className="dgn-score-label">효율 점수</span>
        <div className="dgn-score-track">
          <div className="dgn-score-fill" style={{ width: `${d.score}%` }}></div>
        </div>
        <div className="dgn-score-num">{d.score}</div>
      </div>
    </div>
  );
}

function GapSidebar() {
  const D = window.GG_DATA;
  return (
    <aside className="gap-side">
      <div className="panel-head">
        <h3>Gap Summary</h3>
        <span className="hint">Live</span>
      </div>
      <div className="gs-body">
        <div className="gs-summary">
          <div className="gs-cell">
            <div className="l">Item Lvl</div>
            <div className="v">{D.CHAR.ilvl.toFixed(1)}</div>
          </div>
          <div className="gs-cell">
            <div className="l">Top 1%</div>
            <div className="v">655.0</div>
          </div>
          <div className="gs-cell">
            <div className="l">Percentile</div>
            <div className="v text">상위 {D.CHAR.percentile}%</div>
          </div>
          <div className="gs-cell">
            <div className="l">Hot Slots</div>
            <div className="v">3</div>
          </div>
        </div>
        <div className="gs-bars">
          {D.STATS.map((s) => {
            const max = s.target * 1.15;
            const cur = (s.current / max) * 100;
            const tgt = (s.target / max) * 100;
            const gap = +(s.target - s.current).toFixed(1);
            return (
              <div key={s.key} className="gs-row">
                <span className="gn">{s.short}</span>
                <div className="gtr">
                  <span style={{ width: `${cur}%` }}></span>
                  <span className="target" style={{ left: `calc(${tgt}% - 0.5px)` }}></span>
                </div>
                <span className="gv">−{gap}{s.unit}</span>
              </div>
            );
          })}
        </div>
      </div>
      <div className="gs-foot">
        <span>SYNC: {D.CHAR.lastUpdated}</span>
        <span className="live"><span className="ldot"></span>LIVE</span>
      </div>
    </aside>
  );
}

function RecommendationsScreen() {
  const [tab, setTab] = useStateR('raid');
  const D = window.GG_DATA;

  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="crumbs">
          <a onClick={() => window.__nav('landing')}>Search</a>
          <span className="sep">/</span>
          <a onClick={() => window.__nav('analysis')}>Analysis</a>
          <span className="sep">/</span>
          <span className="here">Recommendations</span>
          <span className="sep">/</span>
          <span>{D.CHAR.name}</span>
        </div>
        <CharHeader char={D.CHAR} />
      </div>

      <div className="tabs">
        <button className={`tab ${tab === 'raid' ? 'active' : ''}`} onClick={() => setTab('raid')}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 12 L7 2 L12 12 Z" stroke="currentColor" strokeWidth="1.4" fill="none"/>
            <circle cx="7" cy="9" r="1.5" fill="currentColor"/>
          </svg>
          레이드 추천
          <span className="count">{D.RAID.bossCount}</span>
        </button>
        <button className={`tab ${tab === 'mplus' ? 'active' : ''}`} onClick={() => setTab('mplus')}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 7 L7 2 L12 7 L7 12 Z" stroke="currentColor" strokeWidth="1.4" fill="none"/>
          </svg>
          쐐기 추천
          <span className="count">{D.DUNGEONS.length}</span>
        </button>
      </div>

      {tab === 'raid' && (
        <div className="recs-grid">
          <div className="boss-list">
            <div style={{
              display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
              marginBottom: 4
            }}>
              <div>
                <div style={{
                  fontFamily: 'Cinzel, serif', fontSize: 22, fontWeight: 600,
                  letterSpacing: '0.04em'
                }}>
                  {D.RAID.name}
                </div>
                <div style={{
                  fontFamily: 'JetBrains Mono, monospace', fontSize: 11,
                  color: 'var(--text-mute)', letterSpacing: '0.1em', marginTop: 4,
                  textTransform: 'uppercase'
                }}>
                  {D.RAID.nameEn} · {D.RAID.bossCount} 넴드
                </div>
              </div>
              <span style={{
                fontFamily: 'JetBrains Mono, monospace', fontSize: 11,
                color: 'var(--text-mute)', letterSpacing: '0.12em', textTransform: 'uppercase'
              }}>우선순위순 정렬</span>
            </div>
            {[...D.RAID.bosses].sort((a, b) => {
              const order = { high: 0, med: 1, low: 2 };
              return order[a.priority] - order[b.priority];
            }).map((b) => <BossCard key={b.idx} b={b} />)}
          </div>
          <GapSidebar />
        </div>
      )}

      {tab === 'mplus' && (
        <div className="recs-grid">
          <div className="boss-list">
            <div style={{
              display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
              marginBottom: 4
            }}>
              <div>
                <div style={{
                  fontFamily: 'Cinzel, serif', fontSize: 22, fontWeight: 600,
                  letterSpacing: '0.04em'
                }}>
                  Mythic+ Dungeons
                </div>
                <div style={{
                  fontFamily: 'JetBrains Mono, monospace', fontSize: 11,
                  color: 'var(--text-mute)', letterSpacing: '0.1em', marginTop: 4,
                  textTransform: 'uppercase'
                }}>
                  Season 4 · 8 던전 · 효율 점수순
                </div>
              </div>
              <span style={{
                fontFamily: 'JetBrains Mono, monospace', fontSize: 11,
                color: 'var(--text-mute)', letterSpacing: '0.12em', textTransform: 'uppercase'
              }}>주간 보상 기준</span>
            </div>
            {[...D.DUNGEONS].sort((a, b) => b.score - a.score).map((d) => <DungeonCard key={d.idx} d={d} />)}
          </div>
          <GapSidebar />
        </div>
      )}
    </div>
  );
}

window.RecommendationsScreen = RecommendationsScreen;
window.CharHeader = CharHeader;
