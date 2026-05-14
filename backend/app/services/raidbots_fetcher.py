"""Raidbots static data fetcher — instances.json + equippable-items.json"""
import os
from dataclasses import dataclass, field
from typing import Optional

import httpx

from app.constants.inventory_types import map_inventory_type, map_quality
from app.services.murlok import Slot

RAIDBOTS_BASE = "https://www.raidbots.com/static/data"
VALID_TYPES = {"dungeon", "raid"}
HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}


@dataclass
class EncounterDTO:
    raidbots_id: int
    name: str


@dataclass
class InstanceDTO:
    raidbots_id: int
    name_en: str
    type: str  # "dungeon" | "raid"
    encounters: list[EncounterDTO] = field(default_factory=list)


@dataclass
class DropItemDTO:
    item_id: int                   # Blizzard item ID
    name: str
    slot: Optional[Slot]           # None → 워커가 스킵
    quality: Optional[str]         # "epic" | "rare" | None → 워커가 스킵
    base_item_level: Optional[int]
    encounter_raidbots_id: int
    instance_raidbots_id: int


class RaidbotsFetcher:
    def __init__(self, hash_val: Optional[str] = None) -> None:
        self._hash = hash_val or os.environ["RAIDBOTS_HASH"]
        self._base = f"{RAIDBOTS_BASE}/{self._hash}"

    def fetch_instances(self) -> list[InstanceDTO]:
        """instances.json → 양수 id + dungeon/raid 타입만 반환."""
        with httpx.Client(headers=HEADERS, timeout=30) as client:
            r = client.get(f"{self._base}/instances.json")
            r.raise_for_status()

        result: list[InstanceDTO] = []
        for inst in r.json():
            if inst["id"] <= 0 or inst.get("type") not in VALID_TYPES:
                continue
            encounters = [
                EncounterDTO(raidbots_id=enc["id"], name=enc["name"])
                for enc in inst.get("encounters", [])
            ]
            result.append(InstanceDTO(
                raidbots_id=inst["id"],
                name_en=inst["name"],
                type=inst["type"],
                encounters=encounters,
            ))
        return result

    def fetch_drops(self, valid_instance_ids: set[int]) -> list[DropItemDTO]:
        """equippable-items.json → valid_instance_ids에서 드롭되는 아이템만 반환.
        한 아이템이 여러 encounter에서 드롭되면 각각 별도 DropItemDTO로 반환.
        """
        with httpx.Client(headers=HEADERS, timeout=60) as client:
            r = client.get(f"{self._base}/equippable-items.json")
            r.raise_for_status()

        result: list[DropItemDTO] = []
        for item in r.json():
            if not isinstance(item, dict) or not item.get("sources"):
                continue

            slot = map_inventory_type(item.get("inventoryType"))
            quality = map_quality(item.get("quality"))
            base_ilvl: Optional[int] = item.get("itemLevel")

            for src in item["sources"]:
                iid: int = src.get("instanceId", 0)
                eid: Optional[int] = src.get("encounterId")
                if iid not in valid_instance_ids or not eid:
                    continue
                result.append(DropItemDTO(
                    item_id=item["id"],
                    name=item["name"],
                    slot=slot,
                    quality=quality,
                    base_item_level=base_ilvl,
                    encounter_raidbots_id=eid,
                    instance_raidbots_id=iid,
                ))
        return result
