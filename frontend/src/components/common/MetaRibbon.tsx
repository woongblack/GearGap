import { META } from '../../data/mock';

interface MetaRibbonProps {
  onOpen: () => void;
}

export default function MetaRibbon({ onOpen }: MetaRibbonProps) {
  return (
    <div className="meta-ribbon">
      <div className="mr-cell">
        <span className="mr-pulse"></span>
        <span className="mr-label">SYNCED</span>
        <span className="mr-value live">{META.syncedAt}</span>
      </div>
      <span className="mr-divider"></span>
      <div className="mr-cell">
        <span className="mr-label">SAMPLE</span>
        <span className="mr-value">n={META.sampleN.toLocaleString()}</span>
      </div>
      <span className="mr-divider"></span>
      <div className="mr-cell">
        <span className="mr-label">BASIS</span>
        <span className="mr-value">{META.basis}</span>
      </div>
      <span className="mr-divider"></span>
      <div className="mr-cell">
        <span className="mr-label">PATCH</span>
        <span className="mr-value">{META.patch}</span>
      </div>
      <button className="mr-info-btn" onClick={onOpen}>
        How we calculate
      </button>
    </div>
  );
}
