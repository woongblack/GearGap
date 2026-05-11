import type { ApiCharacter, ApiEfficiencyResponse } from './types';

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  /** 캐릭터 조회 — 10분 캐시, cache miss 시 Blizzard API 호출 */
  getCharacter(realm: string, name: string): Promise<ApiCharacter> {
    return request<ApiCharacter>(`/api/v1/characters/${encodeURIComponent(realm)}/${encodeURIComponent(name)}`);
  },

  /** 효율 점수 후보 목록 — 가중치 파라미터로 실시간 재계산 */
  getEfficiency(
    characterId: number,
    weights: { w_dps: number; w_time: number; w_prob: number },
  ): Promise<ApiEfficiencyResponse> {
    const params = new URLSearchParams({
      w_dps: String(weights.w_dps),
      w_time: String(weights.w_time),
      w_prob: String(weights.w_prob),
    });
    return request<ApiEfficiencyResponse>(`/api/v1/efficiency/${characterId}?${params}`);
  },

  health(): Promise<{ status: string }> {
    return request<{ status: string }>('/health');
  },
};
