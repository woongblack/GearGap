// ── Transparency layer: ribbon, drawer, provenance, weights, comparison table ──
const { useState: useStateT, useEffect: useEffectT } = React;

// ── Meta ribbon (every screen) ──
function MetaRibbon({ onOpen }) {
  const M = window.GG_DATA.META;
  return (
    <div className="meta-ribbon">
      <div className="mr-cell">
        <span className="mr-pulse"></span>
        <span className="mr-label">SYNCED</span>
        <span className="mr-value live">{M.syncedAt}</span>
      </div>
      <span className="mr-divider"></span>
      <div className="mr-cell">
        <span className="mr-label">SAMPLE</span>
        <span className="mr-value">n={M.sampleN.toLocaleString()}</span>
      </div>
      <span className="mr-divider"></span>
      <div className="mr-cell">
        <span className="mr-label">BASIS</span>
        <span className="mr-value">{M.basis}</span>
      </div>
      <span className="mr-divider"></span>
      <div className="mr-cell">
        <span className="mr-label">PATCH</span>
        <span className="mr-value">{M.patch}</span>
      </div>
      <button className="mr-info-btn" onClick={onOpen}>
        How we calculate
      </button>
    </div>
  );
}

// ── Meta drawer ──
function MetaDrawer({ open, onClose }) {
  const M = window.GG_DATA.META;
  return (
    <>
      <div className={`meta-drawer-bg ${open ? 'open' : ''}`} onClick={onClose}></div>
      <aside className={`meta-drawer ${open ? 'open' : ''}`}>
        <button className="md-close" onClick={onClose}>×</button>
        <h3>How we calculate</h3>
        <div className="md-sub">Methodology · v0.4.2</div>

        <div className="md-section">
          <div className="md-h">Data sources</div>
          {M.sources.map(s => (
            <div className="md-row" key={s}><span className="k">·</span><span className="v">{s}</span></div>
          ))}
        </div>

        <div className="md-section">
          <div className="md-h">Sample</div>
          <div className="md-row"><span className="k">Logs analyzed</span><span className="v">{M.sampleN.toLocaleString()}</span></div>
          <div className="md-row"><span className="k">Window</span><span className="v">지난 7일</span></div>
          <div className="md-row"><span className="k">Patch</span><span className="v">{M.patch}</span></div>
          <div className="md-row"><span className="k">Synced</span><span className="v">{M.syncedAtFull}</span></div>
        </div>

        <div className="md-section">
          <div className="md-h">Basis</div>
          <div style={{ fontSize: 13, lineHeight: 1.6, color: 'var(--text-dim)' }}>
            <strong style={{ color: 'var(--text)' }}>{M.basis}</strong>
            <span style={{ color: 'var(--text-mute)' }}> · {M.basisNote}</span>
          </div>
        </div>

        <div className="md-section">
          <div className="md-h">Important caveats</div>
          <ul className="md-list">
            {M.notes.map(n => <li key={n}>{n}</li>)}
          </ul>
        </div>

        <div className="md-section" style={{ borderBottom: 'none' }}>
          <div className="md-h">Philosophy</div>
          <div style={{ fontSize: 13, lineHeight: 1.7, color: 'var(--text-dim)' }}>
            우리는 정답을 모릅니다. 이 도구는 흩어진 데이터를 한 화면에 모아주고, 가중치 조절을 당신에게 맡깁니다.
            모든 숫자는 출처를 가지며, 그 숫자가 깨지는 조건을 함께 표시합니다.
          </div>
        </div>
      </aside>
    </>
  );
}

// ── Provenance marker — info circle with hover tooltip ──
function Prov({ label, formula, sampleN, source, ci }) {
  return (
    <span className="prov" tabIndex="0">
      <span className="prov-mark">i</span>
      <span className="prov-tip" role="tooltip">
        <div className="pt-h">{label || 'How calculated'}</div>
        {formula && <div className="pt-formula">{formula}</div>}
        {ci && <div className="pt-row"><span className="k">90% CI</span><span>{ci}</span></div>}
        {sampleN != null && <div className="pt-row"><span className="k">Sample</span><span>n = {sampleN.toLocaleString()}</span></div>}
        {source && <div className="pt-source">{source}</div>}
      </span>
    </span>
  );
}

// ── Weight controls ──
const WEIGHT_DEFAULTS = { dps: 0.5, time: 0.3, drop: 0.2 };

function useWeights() {
  const saved = (() => {
    try { return JSON.parse(localStorage.getItem('gg-weights')) || WEIGHT_DEFAULTS; }
    catch { return WEIGHT_DEFAULTS; }
  })();
  const [w, setW] = useStateT(saved);
  useEffectT(() => {
    try { localStorage.setItem('gg-weights', JSON.stringify(w)); } catch {}
  }, [w]);
  return [w, setW];
}

function WeightControls({ weights, onChange, onReset }) {
  const total = weights.dps + weights.time + weights.drop;
  function set(key, v) {
    onChange({ ...weights, [key]: v });
  }
  const rows = [
    { key: 'dps',  icon: '⚔', name: 'DPS gain',  hintLeft: '실용 우선', hintRight: '이론 최대',
      desc: '예상 DPS 증가량을 얼마나 중요하게 볼지' },
    { key: 'time', icon: '⏱', name: 'Time cost', hintLeft: '바쁨',     hintRight: '시간 충분',
      desc: '획득에 드는 시간을 얼마나 페널티로 볼지 (높을수록 시간 절약 우선)' },
    { key: 'drop', icon: '⚂', name: 'Drop %',    hintLeft: '운에 맡김', hintRight: '확실히',
      desc: '드랍 확률을 얼마나 보수적으로 가중할지' },
  ];
  return (
    <div className="weights">
      <div className="weights-h">
        <div>
          <div className="wh-title">Your weights</div>
          <div className="wh-sub" style={{ marginTop: 4 }}>가중치는 당신의 것</div>
        </div>
        <Prov
          label="가중치"
          formula="score = Σ(weight × normalized_metric)"
          source="가중치는 즉시 정렬에 반영되며 브라우저에 로컬 저장됩니다. 정답은 없습니다 — 당신의 우선순위를 그대로 반영하세요."
        />
      </div>
      {rows.map(r => (
        <div className="weight-row" key={r.key}>
          <div className="wr-top">
            <span className="wr-name"><span className="wr-icon">{r.icon}</span>{r.name}</span>
            <span className="wr-pct">{Math.round((weights[r.key] / total) * 100)}%</span>
          </div>
          <input type="range" min="0" max="100" step="1"
            value={Math.round(weights[r.key] * 100)}
            onChange={(e) => set(r.key, +e.target.value / 100)} />
          <div className="wr-hint">
            <span>{r.hintLeft}</span>
            <span>{r.hintRight}</span>
          </div>
        </div>
      ))}
      <button className="weights-reset" onClick={onReset}>Reset to defaults</button>
    </div>
  );
}

// ── Score calculation: normalize each metric per dataset, blend by weight ──
// Higher score = better under user's preferences. Score is 0–100 informational.
function computeScores(items, weights) {
  if (items.length === 0) return [];
  const dpsMax = Math.max(...items.map(i => i.dpsGain));
  const timeMax = Math.max(...items.map(i => i.timeMin));
  const dropMax = Math.max(...items.map(i => i.dropPct));
  const total = weights.dps + weights.time + weights.drop || 1;
  return items.map(i => {
    const nDps  = i.dpsGain  / dpsMax;
    const nTime = 1 - (i.timeMin / timeMax); // less time = better
    const nDrop = i.dropPct  / dropMax;
    const score = ((nDps * weights.dps) + (nTime * weights.time) + (nDrop * weights.drop)) / total;
    return { ...i, _score: score };
  });
}

// ── Comparison table ──
const COLUMNS = [
  { key: 'activity', label: 'Activity / Source', sortable: false },
  { key: 'item',     label: 'Item',             sortable: false },
  { key: 'dpsGain',  label: 'DPS gain',         sortable: true,  numeric: true },
  { key: 'timeMin',  label: 'Time cost',        sortable: true,  numeric: true, ascDefault: true },
  { key: 'dropPct',  label: 'Drop %',           sortable: true,  numeric: true },
  { key: 'tradeoff', label: 'Tradeoff',         sortable: false },
  { key: '_score',   label: 'Your score',       sortable: true,  numeric: true },
];

function ComparisonTable({ rows, kind, sortKey, sortDir, onSort }) {
  const dpsMax = Math.max(...rows.map(r => r.dpsHigh));
  const timeMax = Math.max(...rows.map(r => r.timeMin));
  const dropMax = Math.max(...rows.map(r => r.dropPct));
  return (
    <table className="cmp-table">
      <thead>
        <tr>
          {COLUMNS.map(c => (
            <th key={c.key}
                className={`${c.sortable ? 'sortable' : ''} ${sortKey === c.key ? 'sorted' : ''}`}
                onClick={() => c.sortable && onSort(c.key)}>
              {c.label}
              {c.sortable && (
                <span className="sort-arrow">{sortKey === c.key ? (sortDir === 'asc' ? '↑' : '↓') : '↕'}</span>
              )}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map(r => (
          <tr key={r.idx + '-' + (r.name || r.nameEn)}>
            <td>
              <div className="cmp-act">
                <div className={`cmp-act-tag ${kind === 'mplus' ? 'mplus' : ''}`}>
                  {kind === 'raid' ? `B${r.idx}` : (r.key || `M${r.idx}`)}
                </div>
                <div>
                  <div className="cmp-act-name">{r.name}</div>
                  <div className="cmp-act-sub">
                    {kind === 'raid'
                      ? `${r.nameEn} · ${window.GG_DATA.DIFFICULTY?.[r.difficulty]?.ko || r.difficulty}`
                      : `${r.nameEn} · ${r.drop}`}
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div className="cmp-item-name">{r.item}</div>
              <div className="cmp-item-sub">{r.slot} · ilvl {r.ilvl}</div>
            </td>
            <td>
              <div className="cmp-metric">
                <div className="cmp-metric-bar">
                  <div className="cmp-metric-fill" style={{ width: `${(r.dpsGain / dpsMax) * 100}%` }}></div>
                </div>
                <div className="cmp-metric-val">
                  +{r.dpsGain.toFixed(2)}%
                  <span className="ci">±{((r.dpsHigh - r.dpsLow) / 2).toFixed(2)}</span>
                </div>
                <Prov
                  label="DPS gain"
                  formula={r.formula}
                  ci={`+${r.dpsLow.toFixed(2)} ~ +${r.dpsHigh.toFixed(2)}%`}
                  sampleN={r.sampleN}
                  source="WCL Top 1% 로그 평균에서 현재 사양 차이를 적분한 추정치. 전투 패턴이 다르면 실제 gain이 달라집니다." />
              </div>
            </td>
            <td>
              <div className="cmp-metric">
                <div className="cmp-metric-bar">
                  <div className="cmp-metric-fill time" style={{ width: `${(r.timeMin / timeMax) * 100}%` }}></div>
                </div>
                <div className="cmp-metric-val">
                  ~{r.timeMin >= 60 ? `${Math.round(r.timeMin/60)}h` : `${r.timeMin}m`}
                  <span className="ci">/주</span>
                </div>
                <Prov
                  label="Time cost"
                  formula="run time × runs to expected drop (95%)"
                  source="평균 런타임 × (1 / drop_pct) · 그룹 큐 시간 별도. 길드 정찰이나 사전 예약 시 단축될 수 있습니다."
                  sampleN={r.sampleN} />
              </div>
            </td>
            <td>
              <div className="cmp-metric">
                <div className="cmp-metric-bar">
                  <div className="cmp-metric-fill drop" style={{ width: `${(r.dropPct / dropMax) * 100}%` }}></div>
                </div>
                <div className="cmp-metric-val">
                  {r.dropPct}%
                  <span className="ci">/run</span>
                </div>
                <Prov
                  label="Drop probability"
                  formula="bonus_roll × loot_table_share × spec_eligibility"
                  source="블리자드 공식 데이터 + 커뮤니티 보고. 토큰/대장간 업그레이드는 별도 계산." />
              </div>
            </td>
            <td>
              <span className={`tradeoff ${r.tradeoff}`}>
                {r.tradeoff === 'strong' ? 'Clear win'
                 : r.tradeoff === 'mixed' ? 'Trade-off'
                 : 'Marginal'}
              </span>
            </td>
            <td>
              <div className="cmp-score">
                {Math.round(r._score * 100)}
                <span className="units">/100</span>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

window.MetaRibbon = MetaRibbon;
window.MetaDrawer = MetaDrawer;
window.Prov = Prov;
window.WeightControls = WeightControls;
window.useWeights = useWeights;
window.computeScores = computeScores;
window.WEIGHT_DEFAULTS = WEIGHT_DEFAULTS;
window.ComparisonTable = ComparisonTable;
