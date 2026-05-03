// ── Mock data shared across screens ──
window.GG_DATA = {
  // Global meta — surfaced as a caveat ribbon on every screen.
  META: {
    syncedAt: '2분 전',
    syncedAtFull: '2026-05-03 14:32 KST',
    sample: 'WCL Top 1% · 1,247 logs · 지난 7일',
    sampleN: 1247,
    basis: '패치워크 기준',
    basisNote: '이동/다을 제외 · 단일 대상 도틀',
    patch: '11.1.5',
    sources: ['Warcraft Logs', 'Raider.IO', 'Blizzard Armory'],
    notes: [
      '디딩 이동이 많은 전투에서는 실제 gain이 다릅니다.',
      '장신구 프록은 단일대상 기준이며 쿼르에서는 순위가 바뀌는 경우가 있습니다.',
      '상위 1% 표본은 항상 최신이 아닙니다.',
    ],
  },

  REALMS: [
    { value: 'azshara', label: '아즈샤라' },
    { value: 'hyjal', label: '하이잘' },
    { value: 'cenarius', label: '세나리우스' },
    { value: 'deathwing', label: '데스윙' },
    { value: 'durotan', label: '듀로탄' },
    { value: 'garona', label: '가로나' },
    { value: 'malganis', label: '말가니스' },
    { value: 'wildhammer', label: '와일드해머' },
    { value: 'zuljin', label: '줄진' },
  ],

  RECENT: [
    { name: 'Thalrion', initial: 'T', spec: 'Frost · Mage', role: 'dps-arcane', ilvl: 642, realm: '아즈샤라', when: '2h ago', gap: '+8 ilvl', gapColor: 'gold' },
    { name: '루나리스', initial: '루', spec: 'Restoration · Druid', role: 'healer', ilvl: 638, realm: '하이잘', when: 'yesterday', gap: '+12 ilvl', gapColor: 'gold' },
    { name: 'Vorath', initial: 'V', spec: 'Protection · Warrior', role: 'tank', ilvl: 651, realm: '줄진', when: '3d ago', gap: '+4 ilvl', gapColor: 'jade' },
    { name: '검은바람', initial: '검', spec: 'Assassination · Rogue', role: 'dps-melee', ilvl: 629, realm: '데스윙', when: '5d ago', gap: '+18 ilvl', gapColor: 'crimson' },
  ],

  // The active analyzed character for screens 2 & 3
  CHAR: {
    name: '아즈모단',
    realm: '아즈샤라',
    region: 'KR',
    classSpec: '흑마법사 · 파멸',
    classKo: '흑마법사',
    specKo: '파멸',
    classRole: 'dps-warlock',
    ilvl: 638.4,
    percentile: 18, // 상위 18%
    score: 2347,
    level: 80,
    avatarInitial: '아',
    lastUpdated: '2분 전',
  },

  // Stat gap (current vs top 1% baseline). Values are illustrative.
  STATS: [
    { key: 'haste',       label: '신속',   ko: '신속',   short: 'HASTE', current: 28.4, target: 34.2, unit: '%', priority: 1 },
    { key: 'crit',        label: '치명타', ko: '치명타', short: 'CRIT',  current: 22.1, target: 24.0, unit: '%', priority: 3 },
    { key: 'mastery',     label: '특화',   ko: '특화',   short: 'MAST',  current: 41.7, target: 49.5, unit: '%', priority: 0 },
    { key: 'versatility', label: '유연성', ko: '유연성', short: 'VERS',  current: 8.6,  target: 9.2,  unit: '%', priority: 4 },
  ],

  SECONDARY: { stamina: 612400, intellect: 38420 },

  SLOTS: [
    { slot: 'head',     ko: '머리',     name: 'Hood of Sundered Veils',       ilvl: 639, gap: 0,  source: 'M+ 12 · Halls' },
    { slot: 'neck',     ko: '목',       name: 'Pendant of Drifting Embers',   ilvl: 632, gap: 7,  source: 'Raid · 2nd' },
    { slot: 'shoulder', ko: '어깨',     name: 'Mantle of the Pyrebound',      ilvl: 626, gap: 13, source: 'Raid · 4th',  hot: true },
    { slot: 'cloak',    ko: '망토',     name: 'Drape of the Hollow King',     ilvl: 636, gap: 3,  source: 'M+ 10' },
    { slot: 'chest',    ko: '가슴',     name: 'Cuirass of the Burning Vow',   ilvl: 639, gap: 0,  source: 'Raid · 6th' },
    { slot: 'wrist',    ko: '손목',     name: 'Bracers of Ashen Wake',        ilvl: 622, gap: 17, source: 'M+ 11',         hot: true },
    { slot: 'hands',    ko: '손',       name: 'Gauntlets of Lingering Smoke', ilvl: 636, gap: 3,  source: 'Raid · 3rd' },
    { slot: 'waist',    ko: '허리',     name: 'Cinch of Whispered Names',     ilvl: 636, gap: 3,  source: 'M+ 10' },
    { slot: 'legs',     ko: '다리',     name: 'Greaves of Wandering Suns',    ilvl: 639, gap: 0,  source: 'Raid · 5th' },
    { slot: 'feet',     ko: '발',       name: 'Treads of the Hollow Vow',     ilvl: 624, gap: 15, source: 'M+ 11',         hot: true },
    { slot: 'ring1',    ko: '반지 1',   name: 'Band of Eternal Ash',          ilvl: 636, gap: 3,  source: 'Raid · 1st' },
    { slot: 'ring2',    ko: '반지 2',   name: 'Loop of Forsworn Pact',        ilvl: 632, gap: 7,  source: 'M+ 9' },
    { slot: 'trinket1', ko: '장신구 1', name: 'Voidshard Reliquary',          ilvl: 639, gap: 0,  source: 'Raid · 7th' },
    { slot: 'trinket2', ko: '장신구 2', name: 'Coil of Hollow Light',         ilvl: 632, gap: 7,  source: 'M+ 10' },
    { slot: 'mainhand', ko: '주무기',   name: 'Staff of Pyric Sundering',     ilvl: 642, gap: 0,  source: 'Raid · 8th' },
    { slot: 'offhand',  ko: '보조',     name: '—',                            ilvl: 0,   gap: 0,  source: '—' },
  ],

  // RAID — original generic raid name, not copying any actual WoW raid title verbatim
  RAID: {
    name: '한밤의 요새',
    nameEn: 'Midnight Bastion',
    bossCount: 8,
    bosses: [
      {
        idx: 1, name: '시드린, 잿불의 부름꾼', nameEn: 'Sidrin the Cinder-Caller',
        item: '재의 어깨갑옷', slot: '어깨', slotKey: 'shoulder',
        ilvl: 645, difficulty: 'heroic', priority: 'high',
        why: '특화 +312 · 가장 큰 갭(13 ilvl) 슬롯 직접 해소',
        gain: '+8.4', stat: '특화',
        dpsGain: 1.42, dpsLow: 1.21, dpsHigh: 1.63,
        timeMin: 110, dropPct: 24, sampleN: 1247,
        formula: 'mean(top1%) − current · weighted by uptime', tradeoff: 'strong'
      },
      {
        idx: 2, name: '어둠의 대모 베일라스', nameEn: 'Matron Veylas',
        item: '잿불 결속의 손목보호대', slot: '손목', slotKey: 'wrist',
        ilvl: 642, difficulty: 'heroic', priority: 'high',
        why: '손목 슬롯 17 ilvl 갭, 신속 +185 동시 해소',
        gain: '+6.1', stat: '신속',
        dpsGain: 1.05, dpsLow: 0.84, dpsHigh: 1.26,
        timeMin: 110, dropPct: 21, sampleN: 1247,
        formula: 'mean(top1%) − current · weighted by uptime', tradeoff: 'strong'
      },
      {
        idx: 3, name: '심연 감시자 토르가스트', nameEn: 'Torgast the Watcher',
        item: '비공의 부적', slot: '목', slotKey: 'neck',
        ilvl: 639, difficulty: 'normal', priority: 'med',
        why: '목 슬롯 갭 보완 + 보조 스텟 분배 양호',
        gain: '+3.2', stat: '신속',
        dpsGain: 0.58, dpsLow: 0.41, dpsHigh: 0.75,
        timeMin: 110, dropPct: 18, sampleN: 1247,
        formula: 'mean(top1%) − current · weighted by uptime', tradeoff: 'mixed'
      },
      {
        idx: 4, name: '가시덩굴 군주 큐란', nameEn: 'Lord Quran',
        item: '잿빛 서약의 가시박힌 다리갑옷', slot: '다리', slotKey: 'legs',
        ilvl: 645, difficulty: 'mythic', priority: 'med',
        why: '다리는 0 ilvl 갭이지만 신화 업그레이드로 BiS 도달',
        gain: '+4.0', stat: '특화',
        dpsGain: 0.71, dpsLow: 0.48, dpsHigh: 0.94,
        timeMin: 240, dropPct: 9, sampleN: 612,
        formula: 'mythic key path, conditional on clear', tradeoff: 'mixed'
      },
      {
        idx: 5, name: '잿불 의례관 카이라', nameEn: 'Ritualist Kaira',
        item: '식어가는 의지의 단검', slot: '주무기', slotKey: 'mainhand',
        ilvl: 645, difficulty: 'heroic', priority: 'low',
        why: '무기 갭 없음, 신화 업그레이드 시에만 효과적',
        gain: '+2.1', stat: '주문력',
        dpsGain: 0.36, dpsLow: 0.18, dpsHigh: 0.54,
        timeMin: 110, dropPct: 16, sampleN: 1247,
        formula: 'mean(top1%) − current · weighted by uptime', tradeoff: 'weak'
      },
      {
        idx: 6, name: '심연의 언약자 모르가', nameEn: 'Sworn Morga',
        item: '서리 빛 흉갑', slot: '가슴', slotKey: 'chest',
        ilvl: 642, difficulty: 'heroic', priority: 'low',
        why: '가슴 갭 없음, 토큰 활용도 높음',
        gain: '+1.6', stat: '특화',
        dpsGain: 0.28, dpsLow: 0.11, dpsHigh: 0.45,
        timeMin: 110, dropPct: 22, sampleN: 1247,
        formula: 'mean(top1%) − current · weighted by uptime', tradeoff: 'weak'
      },
      {
        idx: 7, name: '망각의 수호자 테르넬', nameEn: 'Ternel the Forgotten',
        item: '공허파편 성유물', slot: '장신구', slotKey: 'trinket1',
        ilvl: 645, difficulty: 'heroic', priority: 'med',
        why: '교체 가치 미미하지만 단일 대상 확률 우위',
        gain: '+2.8', stat: '특화',
        dpsGain: 0.49, dpsLow: 0.22, dpsHigh: 0.76,
        timeMin: 110, dropPct: 12, sampleN: 1247,
        formula: 'on-use proc value · single target', tradeoff: 'mixed'
      },
      {
        idx: 8, name: '여명의 종결자, 카르나스', nameEn: 'Karnas, Dawnbreaker',
        item: '한밤의 화염 지팡이', slot: '주무기', slotKey: 'mainhand',
        ilvl: 651, difficulty: 'mythic', priority: 'low',
        why: '최종 보스, 신화 클리어 전제. 장기 BiS',
        gain: '+5.4', stat: '주문력',
        dpsGain: 0.94, dpsLow: 0.61, dpsHigh: 1.27,
        timeMin: 360, dropPct: 4, sampleN: 198,
        formula: 'mythic last boss · conditional on clear', tradeoff: 'mixed'
      },
    ],
  },

  // Mythic+ dungeons — original generic names
  DUNGEONS: [
    {
      idx: 1, name: '잿빛 회랑', nameEn: 'Ashen Halls',
      item: '사라진 베일의 어깨', slot: '어깨', slotKey: 'shoulder',
      ilvl: 639, key: 'M+11', drop: '4번째 보스',
      why: '13 ilvl 갭 즉시 해소 · 주간 보상 가치 1순위',
      score: 92, gain: '+7.8', stat: '특화',
        dpsGain: 1.36, dpsLow: 1.15, dpsHigh: 1.57,
        timeMin: 32, dropPct: 14, sampleN: 842,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'strong'
    },
    {
      idx: 2, name: '서리 침식의 굴', nameEn: 'Frostbound Burrow',
      item: '잿불 결속의 손목', slot: '손목', slotKey: 'wrist',
      ilvl: 639, key: 'M+10', drop: '3번째 보스',
      why: '손목 슬롯 17 ilvl 갭 단번 해소',
      score: 88, gain: '+6.4', stat: '신속',
        dpsGain: 1.11, dpsLow: 0.92, dpsHigh: 1.3,
        timeMin: 30, dropPct: 18, sampleN: 802,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'strong'
    },
    {
      idx: 3, name: '갈래진 신전', nameEn: 'Forked Sanctum',
      item: '공허 발자국', slot: '발', slotKey: 'feet',
      ilvl: 636, key: 'M+9', drop: '마지막 보스',
      why: '발 슬롯 15 ilvl 갭, 신속 +152 보너스',
      score: 81, gain: '+5.6', stat: '신속',
        dpsGain: 0.97, dpsLow: 0.79, dpsHigh: 1.15,
        timeMin: 28, dropPct: 16, sampleN: 776,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'strong'
    },
    {
      idx: 4, name: '망각의 첨탑', nameEn: 'Spire of Forgetting',
      item: '잊혀진 서약 고리', slot: '반지', slotKey: 'ring2',
      ilvl: 636, key: 'M+10', drop: '2번째 보스',
      why: '반지 슬롯 7 ilvl 갭, 보조 스텟 매칭 우수',
      score: 64, gain: '+3.1', stat: '특화',
        dpsGain: 0.54, dpsLow: 0.37, dpsHigh: 0.71,
        timeMin: 30, dropPct: 17, sampleN: 802,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'mixed'
    },
    {
      idx: 5, name: '심연의 도서관', nameEn: 'Library of Echoes',
      item: '잿불 망토', slot: '망토', slotKey: 'cloak',
      ilvl: 636, key: 'M+9', drop: '1번째 보스',
      why: '망토 갭 작음, 부속 효율 보강',
      score: 48, gain: '+1.9', stat: '신속',
        dpsGain: 0.31, dpsLow: 0.18, dpsHigh: 0.44,
        timeMin: 28, dropPct: 19, sampleN: 776,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'weak'
    },
    {
      idx: 6, name: '죽음의 항로', nameEn: 'Deathward Channel',
      item: '심연 응시자 부적', slot: '장신구', slotKey: 'trinket2',
      ilvl: 639, key: 'M+11', drop: '4번째 보스',
      why: '장신구 7 ilvl 교체 가능, 단일 대상 강력',
      score: 71, gain: '+4.2', stat: '특화',
        dpsGain: 0.74, dpsLow: 0.52, dpsHigh: 0.96,
        timeMin: 32, dropPct: 12, sampleN: 842,
        formula: 'on-use proc value · single target', tradeoff: 'mixed'
    },
    {
      idx: 7, name: '광물의 무덤', nameEn: 'Tomb of Ore',
      item: '광물심 가슴갑옷', slot: '가슴', slotKey: 'chest',
      ilvl: 636, key: 'M+8', drop: '3번째 보스',
      why: '가슴 갭 없음, 토큰 활용 권장',
      score: 32, gain: '+0.8', stat: '특화',
        dpsGain: 0.18, dpsLow: 0.06, dpsHigh: 0.3,
        timeMin: 26, dropPct: 21, sampleN: 712,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'weak'
    },
    {
      idx: 8, name: '깊은 정박지', nameEn: 'Deepmoor',
      item: '심해 결속 허리띠', slot: '허리', slotKey: 'waist',
      ilvl: 636, key: 'M+8', drop: '2번째 보스',
      why: '허리 갭 작음, 주간 보상 우선순위 낮음',
      score: 28, gain: '+0.7', stat: '신속',
        dpsGain: 0.14, dpsLow: 0.03, dpsHigh: 0.25,
        timeMin: 26, dropPct: 23, sampleN: 712,
        formula: 'weekly vault path · per-run drop × runs', tradeoff: 'weak'
    },
  ],

  ROLE_COLOR: {
    'dps-arcane': 'var(--steel)',
    'dps-warlock': 'var(--violet)',
    'healer': 'var(--jade)',
    'tank': 'var(--violet)',
    'dps-melee': 'var(--crimson)',
  },
  GAP_COLOR: {
    gold: 'var(--gold)',
    jade: 'var(--jade)',
    crimson: 'var(--crimson)',
  },
  DIFFICULTY: {
    normal: { ko: '일반',   color: 'oklch(0.66 0.08 230)' },
    heroic: { ko: '영웅',   color: 'oklch(0.72 0.13 280)' },
    mythic: { ko: '신화',   color: 'oklch(0.70 0.16 30)' },
  },
};
