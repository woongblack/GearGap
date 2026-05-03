import { Link, useNavigate, useParams } from 'react-router-dom';
import CharHeader from '../components/analysis/CharHeader';
import StatRadar from '../components/analysis/StatRadar';
import StatBars from '../components/analysis/StatBars';
import SlotList from '../components/analysis/SlotList';
import { CHAR, STATS, SLOTS } from '../data/mock';

export default function AnalysisScreen() {
  const navigate = useNavigate();
  const { realm, name } = useParams();
  
  // Use mock data for now. In real app, we'd fetch based on realm/name
  const char = { ...CHAR, name: name || CHAR.name, realm: realm || CHAR.realm };

  return (
    <div className="page-enter">
      <div className="page-header">
        <div className="crumbs">
          <Link to="/">Search</Link>
          <span className="sep">/</span>
          <span className="here">Analysis</span>
          <span className="sep">/</span>
          <span>{char.name} · {char.realm}</span>
        </div>
        <CharHeader char={char} />
      </div>

      <div className="analysis-grid">
        <div className="panel">
          <div className="panel-head">
            <h3>Stat Gap</h3>
            <span className="hint">현재 vs 상위 1%</span>
          </div>
          <div className="radar-wrap">
            <StatRadar stats={STATS} />
          </div>
          <div className="radar-legend">
            <span><span className="swatch cur"></span>Current</span>
            <span><span className="swatch tgt"></span>Top 1% Target</span>
          </div>
          <StatBars stats={STATS} />
        </div>

        <div className="panel">
          <div className="panel-head">
            <h3>Slot Gap</h3>
            <span className="hint">우선순위 3개 강조</span>
          </div>
          <div className="slot-list">
            <SlotList slots={SLOTS} />
          </div>
        </div>
      </div>

      <div className="cta-bar">
        <div className="cta-text">
          <div className="cta-title">3개 슬롯에서 큰 갭이 발견되었습니다</div>
          <div className="cta-sub">
            레이드·쐐기 경로별 <b>예상 gain</b>·<b>시간 비용</b>·<b>드랍 확률</b>을 한 표에 모아드립니다.
          </div>
        </div>
        <button className="cta-btn" onClick={() => navigate(`/c/${char.realm}/${char.name}/recs`)}>
          경로 비교하기
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  );
}
