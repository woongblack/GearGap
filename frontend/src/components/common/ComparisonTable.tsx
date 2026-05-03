import Prov from './Prov';
import type { RaidBoss, Dungeon } from '../../data/types';

const DIFFICULTY_MAP: Record<string, { ko: string; color: string }> = {
  normal: { ko: '일반',   color: 'oklch(0.66 0.08 230)' },
  heroic: { ko: '영웅',   color: 'oklch(0.72 0.13 280)' },
  mythic: { ko: '신화',   color: 'oklch(0.70 0.16 30)' },
};

export type RowData = (RaidBoss | Dungeon) & { _score?: number };

interface ComparisonTableProps {
  rows: RowData[];
  kind: 'raid' | 'mplus';
  sortKey: string;
  sortDir: 'asc' | 'desc';
  onSort: (key: string) => void;
}

const COLUMNS = [
  { key: 'activity', label: 'Activity / Source', sortable: false },
  { key: 'item',     label: 'Item',             sortable: false },
  { key: 'dpsGain',  label: 'DPS gain',         sortable: true,  numeric: true },
  { key: 'timeMin',  label: 'Time cost',        sortable: true,  numeric: true, ascDefault: true },
  { key: 'dropPct',  label: 'Drop %',           sortable: true,  numeric: true },
  { key: 'tradeoff', label: 'Tradeoff',         sortable: false },
  { key: '_score',   label: 'Your score',       sortable: true,  numeric: true },
];

export default function ComparisonTable({ rows, kind, sortKey, sortDir, onSort }: ComparisonTableProps) {
  const dpsMax = Math.max(...rows.map(r => r.dpsHigh || r.dpsGain || 0), 1);
  const timeMax = Math.max(...rows.map(r => r.timeMin || 0), 1);
  const dropMax = Math.max(...rows.map(r => r.dropPct || 0), 1);

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
        {rows.map(r => {
          const dpsGain = r.dpsGain || 0;
          const timeMin = r.timeMin || 0;
          const dropPct = r.dropPct || 0;
          const dpsHigh = r.dpsHigh || 0;
          const dpsLow = r.dpsLow || 0;
          const score = r._score || 0;

          return (
            <tr key={r.idx + '-' + (r.name || r.nameEn)}>
              <td>
                <div className="cmp-act">
                  <div className={`cmp-act-tag ${kind === 'mplus' ? 'mplus' : ''}`}>
                    {kind === 'raid' ? `B${r.idx}` : ((r as Dungeon).key || `M${r.idx}`)}
                  </div>
                  <div>
                    <div className="cmp-act-name">{r.name}</div>
                    <div className="cmp-act-sub">
                      {kind === 'raid'
                        ? `${r.nameEn} · ${DIFFICULTY_MAP[(r as RaidBoss).difficulty]?.ko || (r as RaidBoss).difficulty}`
                        : `${r.nameEn} · ${(r as Dungeon).drop}`}
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
                    <div className="cmp-metric-fill" style={{ width: `${(dpsGain / dpsMax) * 100}%` }}></div>
                  </div>
                  <div className="cmp-metric-val">
                    +{dpsGain.toFixed(2)}%
                    <span className="ci">±{((dpsHigh - dpsLow) / 2).toFixed(2)}</span>
                  </div>
                  <Prov
                    label="DPS gain"
                    formula={r.formula}
                    ci={`+${dpsLow.toFixed(2)} ~ +${dpsHigh.toFixed(2)}%`}
                    sampleN={r.sampleN}
                    source="WCL Top 1% 로그 평균에서 현재 사양 차이를 적분한 추정치. 전투 패턴이 다르면 실제 gain이 달라집니다." />
                </div>
              </td>
              <td>
                <div className="cmp-metric">
                  <div className="cmp-metric-bar">
                    <div className="cmp-metric-fill time" style={{ width: `${(timeMin / timeMax) * 100}%` }}></div>
                  </div>
                  <div className="cmp-metric-val">
                    ~{timeMin >= 60 ? `${Math.round(timeMin/60)}h` : `${timeMin}m`}
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
                    <div className="cmp-metric-fill drop" style={{ width: `${(dropPct / dropMax) * 100}%` }}></div>
                  </div>
                  <div className="cmp-metric-val">
                    {dropPct}%
                    <span className="ci">/run</span>
                  </div>
                  <Prov
                    label="Drop probability"
                    formula="bonus_roll × loot_table_share × spec_eligibility"
                    source="블리자드 공식 데이터 + 커뮤니티 보고. 토큰/대장간 업그레이드는 별도 계산." />
                </div>
              </td>
              <td>
                <span className={`tradeoff ${r.tradeoff || 'mixed'}`}>
                  {r.tradeoff === 'strong' ? 'Clear win'
                   : r.tradeoff === 'mixed' ? 'Trade-off'
                   : 'Marginal'}
                </span>
              </td>
              <td>
                <div className="cmp-score">
                  {Math.round(score * 100)}
                  <span className="units">/100</span>
                </div>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
