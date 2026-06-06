import { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import WeightControls, { useWeights, WEIGHT_DEFAULTS } from '../components/common/WeightControls';
import ComparisonTable from '../components/common/ComparisonTable';
import type { RowData } from '../components/common/ComparisonTable';
import Prov from '../components/common/Prov';
import { CHAR, META, RAID_DATA, DUNGEONS } from '../data/mock';
import { computeScores } from '../utils/scores';

function TradeoffLegend() {
  return (
    <div style={{
      display: 'flex', gap: 18, alignItems: 'center', padding: '12px 16px',
      background: 'var(--bg-deep)', border: '1px solid var(--border-soft)',
      borderRadius: 2, marginBottom: 16, fontSize: 12, color: 'var(--text-mute)',
    }}>
      <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 10,
        letterSpacing: '0.16em', textTransform: 'uppercase' }}>Legend</span>
      <span className="tradeoff strong">Clear win</span>
      <span style={{ fontSize: 11 }}>높은 gain · 낮은 비용 · 합리적 확률</span>
      <span style={{ width: 1, height: 14, background: 'var(--border)' }}></span>
      <span className="tradeoff mixed">Trade-off</span>
      <span style={{ fontSize: 11 }}>한쪽이 강하면 다른 쪽이 약함</span>
      <span style={{ width: 1, height: 14, background: 'var(--border)' }}></span>
      <span className="tradeoff weak">Marginal</span>
      <span style={{ fontSize: 11 }}>기여도 낮음</span>
    </div>
  );
}

function GapSnapshot() {
  return (
    <div className="weights" style={{ marginBottom: 14 }}>
      <div className="weights-h">
        <div>
          <div className="wh-title">Gap snapshot</div>
          <div className="wh-sub" style={{ marginTop: 4 }}>현재 → 상위 1%</div>
        </div>
        <Prov
          label="Snapshot"
          formula="user_stat / top1%_median"
          source="WCL Top 1% 표본의 중앙값 기준. 평균이 아닌 중앙값을 쓰는 이유는 outlier의 영향을 줄이기 위함입니다."
          sampleN={META.sampleN} />
      </div>
      <div className="gs-summary" style={{ marginBottom: 0, padding: 0, background: 'none', border: 'none' }}>
        <div className="gs-cell"><div className="l">Item Lvl</div><div className="v">{CHAR.ilvl.toFixed(1)}</div></div>
        <div className="gs-cell"><div className="l">Top 1%</div><div className="v">655.0</div></div>
        <div className="gs-cell"><div className="l">Δ</div><div className="v" style={{ color: 'var(--gold)' }}>−16.6</div></div>
        <div className="gs-cell"><div className="l">Hot slots</div><div className="v">3</div></div>
      </div>
    </div>
  );
}

function SourcesPanel() {
  return (
    <div className="weights">
      <div className="weights-h">
        <div>
          <div className="wh-title">Data sources</div>
          <div className="wh-sub" style={{ marginTop: 4 }}>출처</div>
        </div>
      </div>
      {META.sources.map(s => (
        <div key={s} style={{
          padding: '8px 0', fontSize: 12, color: 'var(--text-dim)',
          fontFamily: 'JetBrains Mono, monospace', letterSpacing: '0.04em',
          borderBottom: '1px solid var(--border-soft)',
        }}>
          <span style={{ color: 'var(--gold)', marginRight: 8 }}>·</span>{s}
        </div>
      ))}
      <div style={{ marginTop: 10, fontSize: 10, color: 'var(--text-mute)',
        fontFamily: 'JetBrains Mono, monospace', letterSpacing: '0.14em',
        textTransform: 'uppercase' }}>
        Last sync · {META.syncedAt}
      </div>
    </div>
  );
}

export default function RecommendationsScreen() {
  const [tab, setTab] = useState<'raid' | 'mplus'>('raid');
  const [weights, setWeights] = useWeights();
  const [sortKey, setSortKey] = useState('_score');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');

  const rows = useMemo(() => {
    const base = tab === 'raid' ? RAID_DATA.bosses : DUNGEONS;
    const scored = computeScores(base as RowData[], weights);
    return [...scored].sort((a, b) => {
      const av = (a as any)[sortKey];
      const bv = (b as any)[sortKey];
      if (av == null) return 1;
      if (bv == null) return -1;
      return sortDir === 'asc' ? av - bv : bv - av;
    });
  }, [tab, weights, sortKey, sortDir]);

  function onSort(key: string) {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir(key === 'timeMin' ? 'asc' : 'desc');
    }
  }

  return (
    <div className="page-enter" style={{ maxWidth: 1320, margin: '0 auto', padding: '0 24px' }}>
      <div className="page-header">
        <div className="crumbs">
          <Link to="/">Search</Link>
          <span className="sep">/</span>
          <Link to={`/c/${CHAR.realm}/${CHAR.name}`}>Analysis</Link>
          <span className="sep">/</span>
          <span className="here">Compare paths</span>
          <span className="sep">/</span>
          <span>{CHAR.name}</span>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', margin: '8px 0 6px' }}>
        <h2 style={{
          fontFamily: 'Cinzel, serif', fontSize: 28, fontWeight: 600,
          letterSpacing: '0.02em', margin: 0, color: 'var(--text)',
        }}>
          Compare paths to your gear
        </h2>
        <span style={{
          fontFamily: 'JetBrains Mono, monospace', fontSize: 11, color: 'var(--text-mute)',
          letterSpacing: '0.14em', textTransform: 'uppercase',
        }}>
          n = {META.sampleN.toLocaleString()} · {META.basis}
        </span>
      </div>
      <p style={{
        fontSize: 14, color: 'var(--text-dim)', maxWidth: 720, lineHeight: 1.6,
        margin: '0 0 18px',
      }}>
        우리는 정답을 모릅니다. 각 활동의 <strong style={{ color: 'var(--text)' }}>예상 DPS gain</strong>,
        <strong style={{ color: 'var(--text)' }}> 시간 비용</strong>,
        <strong style={{ color: 'var(--text)' }}> 드랍 확률</strong>을 한 표에 모았습니다.
        가중치는 직접 조절하세요. 모든 숫자에는 출처가 있습니다 — <span style={{ color: 'var(--gold)', fontStyle: 'italic' }}>i</span> 마크 위에 마우스를 올려보세요.
      </p>

      <div className="disclaimer">
        <div className="dc-mark">CAVEAT</div>
        <div className="dc-body">
          이 점수는 <strong>당신의 가중치 + 우리의 표본</strong>의 산물입니다.
          표본은 패치워크(이동 없는 단일 대상) 기준이며, 실제 던전·레이드 환경에서는 결과가 달라질 수 있습니다.
          <strong style={{ color: 'var(--gold)' }}> 우리의 추천을 따라야 한다는 부담을 느낄 필요 없습니다.</strong>
          이 도구는 결정을 내려주지 않고, 결정을 내릴 재료를 제공합니다.
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === 'raid' ? 'active' : ''}`} onClick={() => setTab('raid')}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 12 L7 2 L12 12 Z" stroke="currentColor" strokeWidth="1.4" fill="none"/>
            <circle cx="7" cy="9" r="1.5" fill="currentColor"/>
          </svg>
          Raid · {RAID_DATA.name}
          <span className="count">{RAID_DATA.bossCount}</span>
        </button>
        <button className={`tab ${tab === 'mplus' ? 'active' : ''}`} onClick={() => setTab('mplus')}>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 7 L7 2 L12 7 L7 12 Z" stroke="currentColor" strokeWidth="1.4" fill="none"/>
          </svg>
          Mythic+ · Season 4
          <span className="count">{DUNGEONS.length}</span>
        </button>
        <span style={{ flex: 1 }}></span>
        <span className="tabs-sub">Sort: <span style={{ color: 'var(--gold)' }}>{
          sortKey === '_score' ? 'Your score' :
          sortKey === 'dpsGain' ? 'DPS gain' :
          sortKey === 'timeMin' ? 'Time cost' :
          sortKey === 'dropPct' ? 'Drop %' : sortKey
        }</span> {sortDir === 'asc' ? '↑' : '↓'}</span>
      </div>

      <div className="recs-grid" style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 280px', gap: 22 }}>
        <div>
          <TradeoffLegend />
          <ComparisonTable
            rows={rows}
            kind={tab}
            sortKey={sortKey}
            sortDir={sortDir}
            onSort={onSort}
          />
          <div style={{
            marginTop: 16, padding: '12px 16px', background: 'oklch(0.20 0.012 60 / 0.4)',
            border: '1px solid var(--border-soft)', borderRadius: 2,
            fontFamily: 'JetBrains Mono, monospace', fontSize: 10.5, color: 'var(--text-mute)',
            letterSpacing: '0.1em', lineHeight: 1.7,
          }}>
            <div style={{ color: 'var(--gold)', textTransform: 'uppercase', marginBottom: 6 }}>What this table is not</div>
            <div style={{ textTransform: 'none', letterSpacing: '0.02em', fontFamily: 'Inter, sans-serif', fontSize: 12.5, color: 'var(--text-dim)', lineHeight: 1.6 }}>
              · 절대적 우선순위가 아닙니다. 즐기는 콘텐츠를 하세요.<br/>
              · 길드 일정, 친구, 파티 가용성 같은 사회적 요소는 반영되지 않습니다.<br/>
              · 패치 변경 시 표본이 갱신될 때까지 며칠 지연될 수 있습니다.
            </div>
          </div>
        </div>

        <aside>
          <WeightControls
            weights={weights}
            onChange={setWeights}
            onReset={() => setWeights(WEIGHT_DEFAULTS)}
          />
          <GapSnapshot />
          <SourcesPanel />
        </aside>
      </div>
    </div>
  );
}
