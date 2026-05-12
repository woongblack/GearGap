from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from typing import Literal, Protocol

import httpx
from bs4 import BeautifulSoup


class Slot(StrEnum):
    HEAD = "head"
    NECK = "neck"
    SHOULDERS = "shoulders"
    BACK = "back"
    CHEST = "chest"
    WRIST = "wrist"
    HANDS = "hands"
    WAIST = "waist"
    LEGS = "legs"
    FEET = "feet"
    RINGS = "rings"
    TRINKETS = "trinkets"
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"


# Murlok HTML 슬롯명 → 도메인 Slot
MURLOK_TO_SLOT: dict[str, Slot] = {
    "Head": Slot.HEAD,
    "Neck": Slot.NECK,
    "Shoulders": Slot.SHOULDERS,
    "Back": Slot.BACK,
    "Chest": Slot.CHEST,
    "Wrist": Slot.WRIST,
    "Hands": Slot.HANDS,
    "Waist": Slot.WAIST,
    "Legs": Slot.LEGS,
    "Feet": Slot.FEET,
    "Rings": Slot.RINGS,
    "Trinkets": Slot.TRINKETS,
    "Main Hand": Slot.MAIN_HAND,
    "Off Hand": Slot.OFF_HAND,
}

# Blizzard API 슬롯 타입 → 도메인 Slot
BLIZZARD_TO_SLOT: dict[str, Slot] = {
    "HEAD": Slot.HEAD,
    "NECK": Slot.NECK,
    "SHOULDER": Slot.SHOULDERS,
    "BACK": Slot.BACK,
    "CHEST": Slot.CHEST,
    "WRIST": Slot.WRIST,
    "HANDS": Slot.HANDS,
    "WAIST": Slot.WAIST,
    "LEGS": Slot.LEGS,
    "FEET": Slot.FEET,
    "FINGER_1": Slot.RINGS,
    "FINGER_2": Slot.RINGS,
    "TRINKET_1": Slot.TRINKETS,
    "TRINKET_2": Slot.TRINKETS,
    "MAIN_HAND": Slot.MAIN_HAND,
    "OFF_HAND": Slot.OFF_HAND,
}


@dataclass
class ItemPopularity:
    class_name: str       # "warlock"
    spec_name: str        # "destruction"
    content_type: str     # "mythic-plus" | "raid"
    slot: Slot
    item_name: str
    item_id: int
    count: int
    total_sample: int     # 항상 50 (Murlok 기준)
    scraped_at: datetime

    def __post_init__(self) -> None:
        if not (0 <= self.count <= self.total_sample):
            raise ValueError(
                f"count {self.count} out of range [0, {self.total_sample}] "
                f"— HTML 구조 변경 감지 ({self.class_name}/{self.spec_name} {self.slot})"
            )


class BiSDataSource(Protocol):
    async def get_slot_popularity(
        self,
        class_name: str,
        spec_name: str,
        content_type: Literal["mythic-plus", "raid"],
    ) -> list[ItemPopularity]: ...


class MurlokScraper:
    """Murlok.io HTML 파서 — BiSDataSource MVP 구현체"""

    BASE_URL = "https://murlok.io"
    HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}
    _TOTAL_SAMPLE_RE = re.compile(r"top\s+(\d+)", re.I)
    _ITEM_ID_RE = re.compile(r"/item=(\d+)")
    _COUNT_RE = re.compile(r"^(\d+)$")

    async def get_slot_popularity(
        self,
        class_name: str,
        spec_name: str,
        content_type: Literal["mythic-plus", "raid"] = "mythic-plus",
    ) -> list[ItemPopularity]:
        url = f"{self.BASE_URL}/{class_name}/{spec_name}/m+"
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url, headers=self.HEADERS, follow_redirects=True, timeout=15
            )
            r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        total_sample = self._parse_total_sample(soup)
        now = datetime.now(timezone.utc)

        return self._parse_slots(soup, class_name, spec_name, content_type, total_sample, now)

    def _parse_total_sample(self, soup: BeautifulSoup) -> int:
        for text in soup.find_all(string=self._TOTAL_SAMPLE_RE):
            m = self._TOTAL_SAMPLE_RE.search(text.strip())
            if m:
                return int(m.group(1))
        return 50  # fallback — 구조 변경 시 __post_init__ assert가 감지

    def _parse_slots(
        self,
        soup: BeautifulSoup,
        class_name: str,
        spec_name: str,
        content_type: str,
        total_sample: int,
        now: datetime,
    ) -> list[ItemPopularity]:
        section = soup.find("section", class_="wow-equipment-slots")
        if not section:
            return []

        results: list[ItemPopularity] = []
        for box in section.find_all("div", recursive=False):
            h3 = box.find("h3")
            if not h3:
                continue
            slot = MURLOK_TO_SLOT.get(h3.text.strip())
            if slot is None:
                continue
            ol = box.find("ol")
            if not ol:
                continue
            for li in ol.find_all("li", class_="vi-poppable", recursive=False):
                item = self._parse_item(
                    li, class_name, spec_name, content_type, slot, total_sample, now
                )
                if item is not None:
                    results.append(item)

        return results

    def _parse_item(
        self,
        li: BeautifulSoup,
        class_name: str,
        spec_name: str,
        content_type: str,
        slot: Slot,
        total_sample: int,
        now: datetime,
    ) -> ItemPopularity | None:
        a = li.find("a", href=self._ITEM_ID_RE)
        if not a:
            return None
        item_id_m = self._ITEM_ID_RE.search(a.get("href", ""))
        if not item_id_m:
            return None

        h4 = li.find("h4")
        if not h4:
            return None

        count = self._parse_count(li)
        if count is None:
            return None

        return ItemPopularity(
            class_name=class_name,
            spec_name=spec_name,
            content_type=content_type,
            slot=slot,
            item_name=h4.text.strip(),
            item_id=int(item_id_m.group(1)),
            count=count,
            total_sample=total_sample,
            scraped_at=now,
        )

    def _parse_count(self, li: BeautifulSoup) -> int | None:
        ul = li.find("ul")
        if not ul:
            return None
        for candidate in reversed(ul.find_all("li", recursive=False)):
            for svg in candidate.find_all("svg"):
                svg.decompose()
            m = self._COUNT_RE.match(candidate.get_text(strip=True))
            if m:
                return int(m.group(1))
        return None
