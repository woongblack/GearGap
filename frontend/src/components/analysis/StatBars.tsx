import type { StatGap } from '../../data/types';

interface StatBarsProps {
  stats: StatGap[];
}

export default function StatBars({ stats }: StatBarsProps) {
  return (
    <div className="stat-bars">
      {stats.map((s) => {
        const max = s.target * 1.15;
        const curPct = (s.current / max) * 100;
        const tgtPct = (s.target / max) * 100;
        const gap = +(s.target - s.current).toFixed(1);
        const high = gap >= 5;
        return (
          <div key={s.key} className={`stat-row ${high ? 'high' : ''}`}>
            <span className="name">{s.short}</span>
            <div className="stat-track">
              <div className="stat-fill" style={{ width: `${curPct}%` }}></div>
              <div className="stat-target-mark" style={{ left: `calc(${tgtPct}% - 1px)` }}></div>
            </div>
            <div className="stat-vals">
              <span className="cur">{s.current}{s.unit}</span>
              <span className={`gap ${high ? 'high' : ''}`}>−{gap}{s.unit}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
