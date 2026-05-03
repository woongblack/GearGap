import type { Weights } from '../components/common/WeightControls';
import type { RowData } from '../components/common/ComparisonTable';

export function computeScores(items: RowData[], weights: Weights): RowData[] {
  if (items.length === 0) return [];
  const dpsMax = Math.max(...items.map(i => i.dpsGain || 0), 1);
  const timeMax = Math.max(...items.map(i => i.timeMin || 0), 1);
  const dropMax = Math.max(...items.map(i => i.dropPct || 0), 1);
  const total = weights.dps + weights.time + weights.drop || 1;
  
  return items.map(i => {
    const nDps  = (i.dpsGain || 0) / dpsMax;
    const nTime = 1 - ((i.timeMin || 0) / timeMax); // less time = better
    const nDrop = (i.dropPct || 0) / dropMax;
    const score = ((nDps * weights.dps) + (nTime * weights.time) + (nDrop * weights.drop)) / total;
    return { ...i, _score: score };
  });
}
