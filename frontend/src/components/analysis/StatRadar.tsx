import type { StatGap } from '../../data/types';

interface StatRadarProps {
  stats: StatGap[];
}

export default function StatRadar({ stats }: StatRadarProps) {
  const size = 360;
  const cx = size / 2, cy = size / 2;
  const radius = 130;
  const n = stats.length;
  const angleFor = (i: number) => (Math.PI * 2 * i / n) - Math.PI / 2;

  // Normalize: max display = 1.15 × target (so target sits ~0.87 on the axis)
  const maxFor = (s: StatGap) => s.target * 1.15;

  const pt = (i: number, ratio: number) => {
    const a = angleFor(i);
    return [cx + Math.cos(a) * radius * ratio, cy + Math.sin(a) * radius * ratio];
  };

  const targetPath = stats.map((s, i) => pt(i, s.target / maxFor(s))).map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ') + ' Z';
  const currentPath = stats.map((s, i) => pt(i, s.current / maxFor(s))).map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ') + ' Z';

  const rings = [0.25, 0.5, 0.75, 1.0];

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="radar-svg" aria-label="Stat radar">
      <g className="radar-grid">
        {rings.map((r, i) => <polygon key={i} points={stats.map((_, j) => pt(j, r).join(',')).join(' ')} />)}
        {stats.map((_, i) => {
          const [x, y] = pt(i, 1);
          return <line key={i} x1={cx} y1={cy} x2={x} y2={y} />;
        })}
      </g>
      <path className="radar-target" d={targetPath} />
      <path className="radar-current" d={currentPath} />
      {stats.map((s, i) => {
        const [x, y] = pt(i, s.current / maxFor(s));
        return <circle key={i} className="radar-current-pt" cx={x} cy={y} r={3.5} />;
      })}
      {stats.map((s, i) => {
        const [x, y] = pt(i, 1.18);
        return (
          <text key={i} x={x} y={y} className="radar-axis-label"
                textAnchor="middle" dominantBaseline="middle">
            {s.short}
          </text>
        );
      })}
    </svg>
  );
}
