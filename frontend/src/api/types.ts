// Backend API response types (aligned with backend/app/schemas/)

export interface ApiCharacter {
  id: number;
  name: string;
  realm: string;
  class_name: string | null;
  spec_name: string | null;
  item_level: number | null;
  last_synced_at: string | null;
  from_cache: boolean;
}

export interface ApiWeights {
  w_dps: number;
  w_time: number;
  w_prob: number;
}

export interface ApiEvidence {
  dps_gain: number;
  dps_source: string;       // e.g. "bloodmallet"
  dps_sim_date: string;
  dps_sim_profile: string;  // e.g. "patchwerk" → UI: "⚠️ 패치워크 기준"
  avg_clear_minutes: number;
  time_source: string;
  drop_rate: number;
  drop_source: string;
  formula: string;
}

export interface ApiCandidate {
  content_id: number;
  content_name: string;
  content_type: 'raid' | 'mythic_plus';
  difficulty: string;
  item_id: number;
  item_name: string;
  item_name_kr: string | null;
  slot: string;
  boss_name: string | null;
  efficiency_score: number;
  evidence: ApiEvidence;
}

export interface ApiEfficiencyResponse {
  character_name: string;
  spec_name: string;
  patch_version: string;
  weights: ApiWeights;
  candidates: ApiCandidate[];
}

export interface ApiError {
  detail: string;
}
