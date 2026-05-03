import { useState, useEffect } from 'react';
import Prov from './Prov';

export interface Weights {
  dps: number;
  time: number;
  drop: number;
}

export const WEIGHT_DEFAULTS: Weights = { dps: 0.5, time: 0.3, drop: 0.2 };

export function useWeights() {
  const saved = (() => {
    try { return JSON.parse(localStorage.getItem('gg-weights') || 'null') || WEIGHT_DEFAULTS; }
    catch { return WEIGHT_DEFAULTS; }
  })();
  const [w, setW] = useState<Weights>(saved);
  useEffect(() => {
    try { localStorage.setItem('gg-weights', JSON.stringify(w)); } catch {}
  }, [w]);
  return [w, setW] as const;
}

interface WeightControlsProps {
  weights: Weights;
  onChange: (w: Weights) => void;
  onReset: () => void;
}

export default function WeightControls({ weights, onChange, onReset }: WeightControlsProps) {
  const total = weights.dps + weights.time + weights.drop;
  function set(key: keyof Weights, v: number) {
    onChange({ ...weights, [key]: v });
  }
  
  const rows: Array<{key: keyof Weights, icon: string, name: string, hintLeft: string, hintRight: string, desc: string}> = [
    { key: 'dps',  icon: '⚔', name: 'DPS gain',  hintLeft: '실용 우선', hintRight: '이론 최대', desc: '예상 DPS 증가량을 얼마나 중요하게 볼지' },
    { key: 'time', icon: '⏱', name: 'Time cost', hintLeft: '바쁨',     hintRight: '시간 충분', desc: '획득에 드는 시간을 얼마나 페널티로 볼지 (높을수록 시간 절약 우선)' },
    { key: 'drop', icon: '⚂', name: 'Drop %',    hintLeft: '운에 맡김', hintRight: '확실히', desc: '드랍 확률을 얼마나 보수적으로 가중할지' },
  ];

  return (
    <div className="weights">
      <div className="weights-h">
        <div>
          <div className="wh-title">Your weights</div>
          <div className="wh-sub" style={{ marginTop: 4 }}>가중치는 당신의 것</div>
        </div>
        <Prov
          label="가중치"
          formula="score = Σ(weight × normalized_metric)"
          source="가중치는 즉시 정렬에 반영되며 브라우저에 로컬 저장됩니다. 정답은 없습니다 — 당신의 우선순위를 그대로 반영하세요."
        />
      </div>
      {rows.map(r => (
        <div className="weight-row" key={r.key}>
          <div className="wr-top">
            <span className="wr-name"><span className="wr-icon">{r.icon}</span>{r.name}</span>
            <span className="wr-pct">{Math.round((weights[r.key] / total) * 100)}%</span>
          </div>
          <input type="range" min="0" max="100" step="1"
            value={Math.round(weights[r.key] * 100)}
            onChange={(e) => set(r.key, +e.target.value / 100)} />
          <div className="wr-hint">
            <span>{r.hintLeft}</span>
            <span>{r.hintRight}</span>
          </div>
        </div>
      ))}
      <button className="weights-reset" onClick={onReset}>Reset to defaults</button>
    </div>
  );
}
