import { useEffect } from 'react';
import { Link, useNavigate, useLocation, useParams } from 'react-router-dom';
import type { ApiRoadmapOut, ApiSlotRoadmapOut } from '../api/types';

const SLOT_LABELS: Record<string, string> = {
  head: 'HEAD', neck: 'NECK', shoulder: 'SHOULDER', back: 'BACK', chest: 'CHEST',
  wrist: 'WRIST', hands: 'HANDS', waist: 'WAIST', legs: 'LEGS', feet: 'FEET',
  finger1: 'RING I', finger2: 'RING II',
  trinket1: 'TRINKET I', trinket2: 'TRINKET II',
  main_hand: 'MAIN HAND', off_hand: 'OFF HAND',
};

function SlotRow({ s }: { s: ApiSlotRoadmapOut }) {
  const top = s.bis_candidates[0];
  const pct = top ? `${top.count}/${top.total_sample}` : '—';
  const sources = top?.drop_sources.map(d => `${d.instance_name} › ${d.encounter_name}`).join(', ') || '—';

  return (
    <tr className={s.is_bis ? 'slot-row-bis' : 'slot-row-gap'}>
      <td className="col-slot">{SLOT_LABELS[s.slot] ?? s.slot}</td>
      <td className="col-my">
        {s.my_item_name ?? <span className="empty">없음</span>}
        {s.my_item_level != null && <span className="ilvl"> ({s.my_item_level})</span>}
      </td>
      <td className="col-bis">
        {top ? top.item_name : <span className="empty">데이터 없음</span>}
      </td>
      <td className="col-pct">{pct}</td>
      <td className="col-src">{sources}</td>
    </tr>
  );
}

export default function AnalysisScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { realm, name } = useParams<{ realm: string; name: string }>();
  const roadmap = (location.state as { roadmap?: ApiRoadmapOut } | null)?.roadmap;

  useEffect(() => {
    if (!roadmap) {
      navigate('/', { replace: true });
    }
  }, [roadmap, navigate]);

  if (!roadmap) return null;

  const scrapedAt = roadmap.scraped_at
    ? new Date(roadmap.scraped_at).toLocaleDateString('ko-KR')
    : '—';
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

        <div className="analysis-meta">
          <span className="meta-tag">{roadmap.class_name} · {roadmap.spec_name}</span>
          <span className="meta-tag">{roadmap.content_type}</span>
          <span className="meta-hint">Murlok.io 기준, 상위 50명 · 갱신 {scrapedAt}</span>
        </div>
      </div>

      <div className="analysis-summary">
        <span className="summary-gap">갭 슬롯 <strong>{gapSlots.length}</strong></span>
        <span className="summary-sep">/</span>
        <span className="summary-total">전체 {roadmap.slots.length}슬롯</span>
      </div>

      <div className="panel">
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
                <th>BiS 후보</th>
                <th>착용률</th>
                <th>드롭처</th>
              </tr>
            </thead>
            <tbody>
              {gapSlots.map(s => <SlotRow key={s.slot} s={s} />)}
              {bisSlots.length > 0 && (
                <tr className="divider-row">
                  <td colSpan={5}>— 이미 BiS 착용 중 —</td>
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
