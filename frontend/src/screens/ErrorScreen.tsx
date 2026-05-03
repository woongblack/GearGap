import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ErrorCard from '../components/common/ErrorCard';
import type { ErrorCase } from '../components/common/ErrorCard';

const ERROR_CASES: ErrorCase[] = [
  {
    kind: 'notfound',
    code: '404',
    title: 'Character Not Found',
    desc: '아즈모단 캐릭터를 아즈샤라 서버에서 찾을 수 없습니다. 이름이나 서버가 맞는지 확인해주세요. 캐릭터를 최근에 서버 이전했거나 이름을 변경한 경우, 전투정보실 갱신에 시간이 걸릴 수 있습니다.',
    primary: { label: '다른 캐릭터 검색', action: 'search' },
    accent: 'gold'
  },
  {
    kind: 'api',
    code: '503',
    title: 'Blizzard API Timeout',
    desc: '블리자드 서버에서 응답이 지연되고 있습니다. 잠시 후 다시 시도해주세요.',
    primary: { label: '다시 시도 (Retry)', action: 'retry' },
    secondary: { label: '메인으로', action: 'search' },
    accent: 'crimson'
  },
  {
    kind: 'unsupported',
    code: '422',
    title: 'Level 80 Required',
    desc: '현재 만렙(80) 캐릭터만 분석을 지원합니다. 레벨업 중인 캐릭터의 경우 엔드게임 데이터(1% 상위) 표본과 비교할 수 없습니다.',
    primary: { label: '뒤로 가기', action: 'search' },
    accent: 'steel'
  }
];

export default function ErrorScreen() {
  const navigate = useNavigate();
  const [caseIdx, setCaseIdx] = useState(0);

  function handleAction(action: string) {
    if (action === 'search') {
      navigate('/');
    } else if (action === 'retry') {
      // For now, simulate retry success by going to analysis
      navigate('/c/azshara/아즈모단');
    }
  }

  return (
    <div className="page-enter" style={{ minHeight: '80vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <ErrorCard c={ERROR_CASES[caseIdx]} onAction={handleAction} />
      
      <div style={{ marginTop: 40, display: 'flex', gap: 8 }}>
        {ERROR_CASES.map((_, i) => (
          <button key={i}
            onClick={() => setCaseIdx(i)}
            style={{
              width: 8, height: 8, borderRadius: '50%',
              background: i === caseIdx ? 'var(--gold)' : 'var(--border)',
              border: 'none', cursor: 'pointer', padding: 0
            }}
            aria-label={`Show error case ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
