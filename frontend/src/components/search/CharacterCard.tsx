import type { RecentChar } from '../../data/types';
import { useNavigate } from 'react-router-dom';

interface CharacterCardProps {
  c: RecentChar;
}

const ROLE_COLOR = {
  'dps-arcane': 'var(--steel)',
  'dps-warlock': 'var(--violet)',
  'healer': 'var(--jade)',
  'tank': 'var(--violet)',
  'dps-melee': 'var(--crimson)',
};

const GAP_COLOR = {
  gold: 'var(--gold)',
  jade: 'var(--jade)',
  crimson: 'var(--crimson)',
};

export default function CharacterCard({ c }: CharacterCardProps) {
  const navigate = useNavigate();
  const color = ROLE_COLOR[c.role];
  const gapColor = GAP_COLOR[c.gapColor];

  return (
    <div 
      className="char-card" 
      style={{ '--class-color': color, '--gap-color': gapColor } as React.CSSProperties}
      onClick={() => navigate(`/c/${c.realm}/${c.name}`)}
    >
      <div className="char-gap"><span className="arrow">↗</span><span>{c.gap}</span></div>
      <div className="char-top">
        <div className="char-portrait">{c.initial}</div>
        <div className="char-info">
          <div className="char-name">{c.name}</div>
          <div className="char-spec">{c.spec}</div>
        </div>
      </div>
      <div className="char-meta">
        <div>
          <span className="char-ilvl"><span className="lbl">item lvl</span>{c.ilvl}</span>
        </div>
        <div className="char-server">
          <div className="char-server-name">{c.realm}</div>
          <div className="char-server-ts">{c.when}</div>
        </div>
      </div>
    </div>
  );
}
