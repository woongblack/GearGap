import { useNavigate, useLocation } from 'react-router-dom';

export default function ErrorScreen() {
  const navigate = useNavigate();
  const location = useLocation();
  const { message, charName, realm } = (location.state as {
    message?: string;
    charName?: string;
    realm?: string;
  }) ?? {};

  function title() {
    if (!message) return '오류가 발생했습니다';
    if (message.includes('찾을 수 없')) return 'Character Not Found';
    if (message.includes('시간 초과') || message.includes('Timeout')) return 'Blizzard API Timeout';
    if (message.includes('힐러') || message.includes('탱커') || message.includes('DPS')) return '미지원 스펙';
    return '오류가 발생했습니다';
  }

  function desc() {
    if (!message) return '알 수 없는 오류입니다. 잠시 후 다시 시도해주세요.';
    if (message.includes('찾을 수 없')) {
      const who = charName ? `${charName} 캐릭터` : '해당 캐릭터';
      const where = realm ? ` (${realm} 서버)` : '';
      return `${who}를${where} 찾을 수 없습니다. 이름이나 서버가 맞는지 확인해주세요. 최근 서버 이전이나 이름 변경 시 전투정보실 갱신에 시간이 걸릴 수 있습니다.`;
    }
    if (message.includes('시간 초과') || message.includes('Timeout')) {
      return '블리자드 서버에서 응답이 지연되고 있습니다. 잠시 후 다시 시도해주세요.';
    }
    if (message.includes('힐러') || message.includes('탱커') || message.includes('DPS')) {
      return 'DPS 스펙만 지원합니다. 힐러/탱커 캐릭터는 현재 지원하지 않습니다.';
    }
    return message;
  }

  return (
    <div className="page-enter" style={{
      minHeight: '80vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', gap: 24,
    }}>
      <div style={{
        background: 'var(--bg-card)', border: '1px solid var(--border)',
        borderRadius: 4, padding: '40px 48px', maxWidth: 520, width: '100%',
        textAlign: 'center',
      }}>
        <div style={{
          fontFamily: 'JetBrains Mono, monospace', fontSize: 11,
          color: 'var(--text-mute)', letterSpacing: '0.16em',
          textTransform: 'uppercase', marginBottom: 16,
        }}>
          {message?.includes('찾을 수 없') ? '404' : message?.includes('시간 초과') ? '502' : 'Error'}
        </div>
        <h2 style={{
          fontFamily: 'Cinzel, serif', fontSize: 22, color: 'var(--gold)',
          marginBottom: 16,
        }}>
          {title()}
        </h2>
        <p style={{
          fontSize: 14, color: 'var(--text-dim)', lineHeight: 1.7,
          marginBottom: 32,
        }}>
          {desc()}
        </p>
        <button
          onClick={() => navigate('/')}
          className="search-btn"
          style={{ width: '100%', justifyContent: 'center' }}
        >
          다른 캐릭터 검색
        </button>
      </div>
    </div>
  );
}
