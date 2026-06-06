import { useState, useEffect } from 'react';
import SearchPanel from '../components/search/SearchPanel';
import { loadRecentSearches } from '../App';
import { REALMS } from '../data/mock';

interface LandingScreenProps {
  onSearch: (data: { name: string; realm: string }) => void;
}

export default function LandingScreen({ onSearch }: LandingScreenProps) {
  const [recents, setRecents] = useState<{ name: string; realm: string; searchedAt: string }[]>([]);

  useEffect(() => {
    setRecents(loadRecentSearches());
  }, []);

  function realmLabel(value: string) {
    return REALMS.find(r => r.value === value)?.label ?? value;
  }

  function timeAgo(iso: string) {
    const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
    if (diff < 60) return '방금 전';
    if (diff < 3600) return `${Math.floor(diff / 60)}분 전`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`;
    return `${Math.floor(diff / 86400)}일 전`;
  }

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

      {recents.length > 0 && (
        <section className="section">
          <div className="section-head">
            <div className="section-title">
              <span className="ornament"></span>
              <h2>Recent Searches</h2>
              <span className="ornament"></span>
            </div>
          </div>
          <div className="recent-grid">
            {recents.map(r => (
              <div
                key={`${r.realm}-${r.name}`}
                className="char-card"
                onClick={() => onSearch({ name: r.name, realm: r.realm })}
                style={{ cursor: 'pointer' }}
              >
                <div className="char-top">
                  <div className="char-portrait">{r.name.charAt(0).toUpperCase()}</div>
                  <div className="char-info">
                    <div className="char-name">{r.name}</div>
                    <div className="char-spec">{realmLabel(r.realm)}</div>
                  </div>
                </div>
                <div className="char-meta">
                  <div className="char-server">
                    <div className="char-server-ts">{timeAgo(r.searchedAt)}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
