import { useEffect, useState } from 'react';
import { Link, useNavigate, useLocation, useParams } from 'react-router-dom';
import type { ApiRoadmapOut, ApiSlotRoadmapOut } from '../api/types';
import CharHeader from '../components/analysis/CharHeader';
import { api } from '../api/client';

const SLOT_LABELS: Record<string, string> = {
  head: 'Head', neck: 'Neck', shoulder: 'Shoulder', back: 'Back', chest: 'Chest',
  wrist: 'Wrist', hands: 'Hands', waist: 'Waist', legs: 'Legs', feet: 'Feet',
  finger1: 'Ring I', finger2: 'Ring II',
  trinket1: 'Trinket I', trinket2: 'Trinket II',
  main_hand: 'Main Hand', off_hand: 'Off Hand',
};

function BisBar({ count, total }: { count: number; total: number }) {
  const pct = Math.round((count / total) * 100);
  return (
    <div className="bis-bar-row">
      <div className="bis-bar-track">
        <div className="bis-bar-fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="bis-bar-pct">{pct}%</span>
    </div>
  );
}

function SlotRow({ s }: { s: ApiSlotRoadmapOut }) {
  const [expanded, setExpanded] = useState(!s.is_bis);
  const top = s.bis_candidates[0];
  const visible = expanded ? s.bis_candidates.slice(0, 3) : s.bis_candidates.slice(0, 1);

  return (
    <tr
      className={`${s.is_bis ? 'slot-row-bis' : 'slot-row-gap'}${expanded ? ' expanded' : ''}`}
      onClick={() => setExpanded(e => !e)}
    >
      <td className="col-slot">
        {s.is_bis && <span className="bis-check">✓</span>}
        {SLOT_LABELS[s.slot] ?? s.slot}
        {s.bis_candidates.length > 1 && (
          <span className={`row-chevron${expanded ? ' open' : ''}`}>›</span>
        )}
      </td>
      <td className="col-my">
        {s.my_item_name ?? <span className="empty">없음</span>}
        {s.my_item_level != null && <span className="ilvl"> ({s.my_item_level})</span>}
      </td>
      <td className="col-bis-list">
        {visible.length === 0 ? (
          <span className="empty">데이터 없음</span>
        ) : (
          visible.map((c, i) => (
            <div key={c.item_id} className={`bis-candidate${i === 0 ? ' is-top' : ''}`}>
              <a
                className="bis-cand-name"
                href={`https://www.wowhead.com/item=${c.item_id}`}
                target="_blank"
                rel="noreferrer"
                onClick={e => e.stopPropagation()}
              >
                {c.icon_url && (
                  <img
                    src={c.icon_url}
                    width={33}
                    height={33}
                    alt=""
                    className="item-icon-img"
                  />
                )}
                <span>{c.item_name}</span>
              </a>
              <BisBar count={c.count} total={c.total_sample} />
            </div>
          ))
        )}
      </td>
      <td className="col-src">
        {top?.source_type === 'unknown'
          ? <span className="src-chip src-unknown">제작/외부</span>
          : top?.drop_sources.length
            ? top.drop_sources.map((d, i) => (
                <span key={i} className="src-chip">
                  <span className="src-instance">{d.instance_name}</span>
                  <span className="src-encounter">› {d.encounter_name}</span>
                </span>
              ))
            : <span className="empty">—</span>
        }
      </td>
    </tr>
  );
}

export default function AnalysisScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { realm, name } = useParams<{ realm: string; name: string }>();
  const stateRoadmap = (location.state as { roadmap?: ApiRoadmapOut } | null)?.roadmap;
  const [roadmap, setRoadmap] = useState<ApiRoadmapOut | null>(stateRoadmap ?? null);
  const [loading, setLoading] = useState(!stateRoadmap);

  useEffect(() => {
    if (stateRoadmap) return;
    if (!realm || !name) { navigate('/'); return; }
    api.getRoadmap(realm, name)
      .then(data => setRoadmap(data))
      .catch(err => navigate('/errors', { state: { message: err.message, charName: name, realm } }))
      .finally(() => setLoading(false));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: 'var(--text-dim)' }}>
      Loading…
    </div>
  );

  if (!roadmap) return null;

  const gapSlots = roadmap.slots.filter(s => !s.is_bis);
  const bisSlots = roadmap.slots.filter(s => s.is_bis);

  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="crumbs">
          <Link to="/">Search</Link>
          <span className="sep">/</span>
          <span className="here">Analysis</span>
          <span className="sep">/</span>
          <span>{name} · {realm}</span>
        </div>
      </div>

      <CharHeader roadmap={roadmap} name={name ?? ''} realm={realm ?? ''} />

      <div className="panel" style={{ marginTop: 24 }}>
        <div className="panel-head">
          <h3>Slot Gap</h3>
          <span className="hint">BiS 후보 착용률 기준 · Murlok.io</span>
        </div>
        <div className="slot-table-wrap">
          <table className="slot-table">
            <thead>
              <tr>
                <th>슬롯</th>
                <th>내 장비</th>
                <th>BiS 후보 (착용률)</th>
                <th>드롭처</th>
              </tr>
            </thead>
            <tbody>
              {gapSlots.map(s => <SlotRow key={s.slot} s={s} />)}
              {bisSlots.length > 0 && (
                <tr className="divider-row">
                  <td colSpan={4}>— 이미 BiS 착용 중 —</td>
                </tr>
              )}
              {bisSlots.map(s => <SlotRow key={s.slot} s={s} />)}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
