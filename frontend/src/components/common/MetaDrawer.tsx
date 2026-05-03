import { META } from '../../data/mock';

interface MetaDrawerProps {
  open: boolean;
  onClose: () => void;
}

export default function MetaDrawer({ open, onClose }: MetaDrawerProps) {
  return (
    <>
      <div className={`meta-drawer-bg ${open ? 'open' : ''}`} onClick={onClose}></div>
      <aside className={`meta-drawer ${open ? 'open' : ''}`}>
        <button className="md-close" onClick={onClose}>×</button>
        <h3>How we calculate</h3>
        <div className="md-sub">Methodology · v0.4.2</div>

        <div className="md-section">
          <div className="md-h">Data sources</div>
          {META.sources.map(s => (
            <div className="md-row" key={s}><span className="k">·</span><span className="v">{s}</span></div>
          ))}
        </div>

        <div className="md-section">
          <div className="md-h">Sample</div>
          <div className="md-row"><span className="k">Logs analyzed</span><span className="v">{META.sampleN.toLocaleString()}</span></div>
          <div className="md-row"><span className="k">Window</span><span className="v">지난 7일</span></div>
          <div className="md-row"><span className="k">Patch</span><span className="v">{META.patch}</span></div>
          <div className="md-row"><span className="k">Synced</span><span className="v">{META.syncedAtFull}</span></div>
        </div>

        <div className="md-section">
          <div className="md-h">Basis</div>
          <div style={{ fontSize: 13, lineHeight: 1.6, color: 'var(--text-dim)' }}>
            <strong style={{ color: 'var(--text)' }}>{META.basis}</strong>
            <span style={{ color: 'var(--text-mute)' }}> · {META.basisNote}</span>
          </div>
        </div>

        <div className="md-section">
          <div className="md-h">Important caveats</div>
          <ul className="md-list">
            {META.notes.map(n => <li key={n}>{n}</li>)}
          </ul>
        </div>

        <div className="md-section" style={{ borderBottom: 'none' }}>
          <div className="md-h">Philosophy</div>
          <div style={{ fontSize: 13, lineHeight: 1.7, color: 'var(--text-dim)' }}>
            우리는 정답을 모릅니다. 이 도구는 흩어진 데이터를 한 화면에 모아주고, 가중치 조절을 당신에게 맡깁니다.
            모든 숫자는 출처를 가지며, 그 숫자가 깨지는 조건을 함께 표시합니다.
          </div>
        </div>
      </aside>
    </>
  );
}
