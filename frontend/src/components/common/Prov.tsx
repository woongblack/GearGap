interface ProvProps {
  label?: string;
  formula?: string;
  sampleN?: number;
  source?: string;
  ci?: string;
}

export default function Prov({ label, formula, sampleN, source, ci }: ProvProps) {
  return (
    <span className="prov" tabIndex={0}>
      <span className="prov-mark">i</span>
      <span className="prov-tip" role="tooltip">
        <div className="pt-h">{label || 'How calculated'}</div>
        {formula && <div className="pt-formula">{formula}</div>}
        {ci && <div className="pt-row"><span className="k">90% CI</span><span>{ci}</span></div>}
        {sampleN != null && <div className="pt-row"><span className="k">Sample</span><span>n = {sampleN.toLocaleString()}</span></div>}
        {source && <div className="pt-source">{source}</div>}
      </span>
    </span>
  );
}
