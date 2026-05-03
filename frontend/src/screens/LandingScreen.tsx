import SearchPanel from '../components/search/SearchPanel';
import CharacterCard from '../components/search/CharacterCard';
import { RECENT } from '../data/mock';

interface LandingScreenProps {
  onSearch: (data: { name: string; realm: string }) => void;
}

export default function LandingScreen({ onSearch }: LandingScreenProps) {
  const visible = RECENT.slice(0, 4);

  return (
    <div className="page-enter">
      <section className="hero">
        <span className="eyebrow">
          <span className="dot"></span>
          Patch 11.1 · Season of Ascension
        </span>
        <h1 className="title">
          Find Your <span className="accent">Gear Gap</span>
        </h1>
        <p className="subtitle">
          상위 <span className="em">1%</span> 템셋 데이터 기반으로 당신의 장비를 분석하고,
          가장 효율적인 <span className="em">레이드 넴드</span>와 <span className="em">쐐기 던전</span>을 추천합니다.
        </p>
        <SearchPanel onSubmit={onSearch} />
        
        <div className="stat-strip">
          <div className="stat"><div className="stat-num">2.4M</div><div className="stat-label">Characters Indexed</div></div>
          <div className="stat"><div className="stat-num">14</div><div className="stat-label">Raid Bosses Tracked</div></div>
          <div className="stat"><div className="stat-num">8</div><div className="stat-label">M+ Dungeons</div></div>
          <div className="stat"><div className="stat-num">11.1.5</div><div className="stat-label">Live Patch</div></div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div className="section-title">
            <span className="ornament"></span>
            <h2>Recent Searches</h2>
            <span className="ornament"></span>
          </div>
          <a className="section-link" style={{ cursor: 'pointer' }}>View All →</a>
        </div>
        <div className="recent-grid">
          {visible.map((c) => (
            <CharacterCard key={c.name} c={c} />
          ))}
        </div>
      </section>
    </div>
  );
}
