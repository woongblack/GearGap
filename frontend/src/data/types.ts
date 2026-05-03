export type ClassRole = 'tank' | 'healer' | 'dps-arcane' | 'dps-warlock' | 'dps-melee';

export interface Realm {
  value: string;
  label: string; // Korean realm name
}

export interface RecentChar {
  name: string;
  initial: string;
  spec: string;
  role: ClassRole;
  ilvl: number;
  realm: string;
  when: string;
  gap: string;
  gapColor: 'gold' | 'jade' | 'crimson';
}

export interface CharProfile {
  name: string;
  realm: string;
  region: 'KR';
  classSpec: string;
  classKo: string;
  specKo: string;
  classRole: ClassRole;
  ilvl: number;
  percentile: number;
  score: number;
  level: number;
  avatarInitial: string;
  lastUpdated: string;
}

export interface StatGap {
  key: 'haste' | 'crit' | 'mastery' | 'versatility';
  label: string;
  ko?: string;
  short: 'HASTE' | 'CRIT' | 'MAST' | 'VERS';
  current: number;
  target: number;
  unit: '%';
  priority: number;
}

export interface SlotItem {
  slot: 'head' | 'neck' | 'shoulder' | 'cloak' | 'chest' | 'wrist' | 'hands'
      | 'waist' | 'legs' | 'feet' | 'ring1' | 'ring2'
      | 'trinket1' | 'trinket2' | 'mainhand' | 'offhand';
  ko: string;
  name: string;
  ilvl: number;
  gap: number;
  source: string;
  hot?: boolean;
}

export type Difficulty = 'normal' | 'heroic' | 'mythic';
export type Priority = 'high' | 'med' | 'low';

export interface RaidBoss {
  idx: number;
  name: string;
  nameEn: string;
  item: string;
  slot: string;       // localized
  slotKey: SlotItem['slot'];
  ilvl: number;
  difficulty: Difficulty;
  priority: Priority;
  why: string;        // AI reason
  gain: string;       // "+8.4"
  stat: string;       // "특화"
  dpsGain?: number;
  dpsLow?: number;
  dpsHigh?: number;
  timeMin?: number;
  dropPct?: number;
  sampleN?: number;
  formula?: string;
  tradeoff?: string;
}

export interface Dungeon {
  idx: number;
  name: string;
  nameEn: string;
  item: string;
  slot: string;
  slotKey: SlotItem['slot'];
  ilvl: number;
  key: string;        // "M+11"
  drop: string;       // "4번째 보스"
  why: string;
  score: number;      // 0-100 efficiency
  gain: string;
  stat: string;
  dpsGain?: number;
  dpsLow?: number;
  dpsHigh?: number;
  timeMin?: number;
  dropPct?: number;
  sampleN?: number;
  formula?: string;
  tradeoff?: string;
}

export interface GlobalMeta {
  syncedAt: string;
  syncedAtFull: string;
  sample: string;
  sampleN: number;
  basis: string;
  basisNote: string;
  patch: string;
  sources: string[];
  notes: string[];
}
