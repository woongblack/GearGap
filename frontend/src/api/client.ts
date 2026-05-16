import type { ApiCharacter, ApiRoadmapOut } from './types';

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

  /** 장비 갭 로드맵 — 슬롯별 BiS 후보 + 드롭처 */
  getRoadmap(realm: string, name: string, contentType = 'mythic-plus'): Promise<ApiRoadmapOut> {
    return request<ApiRoadmapOut>(
      `/api/v1/characters/${encodeURIComponent(realm)}/${encodeURIComponent(name)}/roadmap?content_type=${encodeURIComponent(contentType)}`,
    );
  },

  health(): Promise<{ status: string }> {
    return request<{ status: string }>('/health');
  },
};
