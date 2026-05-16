import type { ApiRoadmapOut } from '../../api/types';

interface CharHeaderProps {
  roadmap: ApiRoadmapOut;
  name: string;
  realm: string;
}

export default function CharHeader({ roadmap, name, realm }: CharHeaderProps) {
  const initial = name.charAt(0).toUpperCase();
  const scrapedAt = roadmap.scraped_at
    ? new Date(roadmap.scraped_at).toLocaleDateString('ko-KR')
    : '—';
  const gapCount = roadmap.slots.filter(s => !s.is_bis).length;
  const totalSlots = roadmap.slots.length;

  return (
    <div className="char-header">
      <div className="ch-portrait">
        <span className="corner tl"></span><span className="corner tr"></span>
        <span className="corner bl"></span><span className="corner br"></span>
        {initial}
      </div>
      <div className="ch-meta">
        <div className="ch-name">{name}</div>
        <div className="ch-tags">
          <span className="ch-tag spec">{roadmap.class_name} · {roadmap.spec_name}</span>
          <span className="ch-tag">{roadmap.content_type}</span>
          <span className="ch-tag">{realm}</span>
          <span className="ch-tag">갱신 {scrapedAt}</span>
        </div>
        <div className="ch-row">
          <div className="ch-stat">
            <span className="l">Data Source</span>
            <span className="v" style={{ fontSize: 14 }}>Murlok.io</span>
          </div>
          <div className="ch-stat">
            <span className="l">Sample</span>
            <span className="v" style={{ fontSize: 14 }}>상위 50명</span>
          </div>
        </div>
      </div>
      <div className="ch-score">
        <div className="pct">{gapCount}<sup style={{ fontSize: 20, verticalAlign: 'super' }}>갭</sup></div>
        <div className="lab">슬롯 / 전체 {totalSlots}</div>
        <div className="sub">갭이 있는 슬롯 수</div>
      </div>
    </div>
  );
}
