import type { SlotItem } from '../../data/types';

interface SlotListProps {
  slots: SlotItem[];
}

const SLOT_LABELS: Record<string, string> = {
  head: 'HEAD', neck: 'NECK', shoulder: 'SHOULDER', cloak: 'BACK', chest: 'CHEST',
  wrist: 'WRIST', hands: 'HANDS', waist: 'WAIST', legs: 'LEGS', feet: 'FEET',
  ring1: 'RING I', ring2: 'RING II', trinket1: 'TRINKET I', trinket2: 'TRINKET II',
  mainhand: 'MAIN', offhand: 'OFF',
};

function SlotRow({ s }: { s: SlotItem }) {
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

export default function SlotList({ slots }: SlotListProps) {
  return (
    <div className="slot-list">
      {slots.map((s) => (
        <SlotRow key={s.slot} s={s} />
      ))}
    </div>
  );
}
