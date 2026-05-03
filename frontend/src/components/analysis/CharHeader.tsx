import type { CharProfile } from '../../data/types';

interface CharHeaderProps {
  char: CharProfile;
}

export default function CharHeader({ char }: CharHeaderProps) {
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
