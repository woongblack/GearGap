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

export interface ApiDropSourceOut {
  instance_name: string;
  encounter_name: string;
  item_level: number | null;
}

export interface ApiBisCandidateOut {
  item_id: number;
  item_name: string;
  icon_url: string | null;
  count: number;
  total_sample: number;
  source_type: 'drop' | 'unknown';
  drop_sources: ApiDropSourceOut[];
}

export interface ApiSlotRoadmapOut {
  slot: string;
  my_item_id: number | null;
  my_item_name: string | null;
  my_item_level: number | null;
  is_bis: boolean;
  bis_candidates: ApiBisCandidateOut[];
}

export interface ApiRoadmapOut {
  character_id: number;
  class_name: string;
  spec_name: string;
  content_type: string;
  scraped_at: string | null;
  slots: ApiSlotRoadmapOut[];
}

export interface ApiError {
  detail: string;
}
